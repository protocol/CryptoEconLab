import numpy as np
import pandas as pd


def forecast_qa_onboardings(
    rb_onboard_power: float, fil_plus_rate: float, forecast_lenght: int, 
    qap_multiplier: float) -> np.array:
    qa_onboard_power = (1 + (qap_multiplier-1) * fil_plus_rate) * rb_onboard_power
    qa_onboarded_power_vec = np.ones(forecast_lenght) * qa_onboard_power
    qa_onboarded_power_vec[0] = 0.0
    return qa_onboarded_power_vec


def forecast_rb_onboardings(rb_onboard_power: float, forecast_lenght: int) -> np.array:
    rb_onboarded_power_vec = np.ones(forecast_lenght) * rb_onboard_power
    rb_onboarded_power_vec[0] = 0.0
    return rb_onboarded_power_vec


def forecast_power_stats(
    power_zero: float,
    known_scheduled_expire_vec: np.array,
    forecast_onboarded_power_vec: np.array,
    renewal_rate: float,
    onboard_length: int,
    renewal_length: int,
    forecast_lenght: int,
) -> pd.DataFrame:
    forecast_steps_vec = np.arange(forecast_lenght)
    onboarded_power_cumsum_vec = forecast_onboarded_power_vec.cumsum()
    forecast_scheduled_expirations_vec = forecast_power_scheduled_expirations(
        forecast_onboarded_power_vec,
        known_scheduled_expire_vec,
        renewal_rate,
        onboard_length,
        renewal_length,
        forecast_lenght,
    )
    expired_power_vec = (1 - renewal_rate) * forecast_scheduled_expirations_vec
    expired_power_cumsum_vec = expired_power_vec.cumsum()
    power_zero_vec = np.ones(forecast_lenght) * power_zero
    total_power = power_zero_vec + onboarded_power_cumsum_vec - expired_power_cumsum_vec
    rb_df = pd.DataFrame(
        {
            "forecasting_step": forecast_steps_vec,
            "onboarded_power": forecast_onboarded_power_vec,
            "cum_onboarded_power": onboarded_power_cumsum_vec,
            "expired_power": expired_power_vec,
            "cum_expired_power": expired_power_cumsum_vec,
            "total_power": total_power,
        }
    )
    return rb_df


def forecast_power_scheduled_expirations(
    forecast_onboarded_power_vec: np.array,
    known_scheduled_expire_vec: np.array,
    renewal_rate: float,
    onboard_length: int,
    renewal_length: int,
    forecast_lenght: int,
) -> np.array:
    # Scheduled expirations from known sectors
    known_scheduled_expire_vec_pad = pad_power_scheduled_expirations_from_known_power(
        known_scheduled_expire_vec, forecast_lenght
    )
    # Scheduled expirations from new onboardings
    scheduled_expire_onboard_vec = (
        forecast_power_scheduled_expirations_from_onboarded_power(
            forecast_onboarded_power_vec, onboard_length, forecast_lenght
        )
    )
    # Scheduled expirations from renewals
    scheduled_expire_renew_vec = (
        forecast_power_scheduled_expirations_from_renewed_power(
            forecast_onboarded_power_vec,
            known_scheduled_expire_vec_pad,
            renewal_rate,
            onboard_length,
            renewal_length,
            forecast_lenght,
        )
    )
    # Total scheduled expirations
    total_scheduled_expire_vec = (
        known_scheduled_expire_vec_pad
        + scheduled_expire_onboard_vec
        + scheduled_expire_renew_vec
    )
    return total_scheduled_expire_vec


def pad_power_scheduled_expirations_from_known_power(
    known_scheduled_expire_vec: np.array, forecast_lenght: int
) -> np.array:
    pad_size = forecast_lenght - len(known_scheduled_expire_vec)
    known_scheduled_expire_vec_pad = np.concatenate(
        [known_scheduled_expire_vec, np.zeros(pad_size)]
    )
    return known_scheduled_expire_vec_pad


def forecast_power_scheduled_expirations_from_onboarded_power(
    onboard_power_vec: np.array, onboard_length: int, forecast_lenght: int
) -> np.array:
    schedule_expire_onboard_full_vec = np.concatenate(
        [np.zeros(onboard_length), onboard_power_vec]
    )
    schedule_expire_onboard_vec = schedule_expire_onboard_full_vec[:forecast_lenght]
    return schedule_expire_onboard_vec


def forecast_power_scheduled_expirations_from_renewed_power(
    onboard_power_vec: np.array,
    schedule_expire_known_vec_pad: np.array,
    renewal_rate: float,
    onboard_length: int,
    renewal_length: int,
    forecast_lenght: int,
) -> np.array:
    schedule_expire_renewed_known_full_vec = renewal_rate * np.concatenate(
        [np.zeros(renewal_length), schedule_expire_known_vec_pad]
    )
    schedule_expire_renewed_known_vec = schedule_expire_renewed_known_full_vec[
        :forecast_lenght
    ]
    schedule_expire_renewed_onboards_full_vec = renewal_rate * np.concatenate(
        [np.zeros(onboard_length + renewal_length), onboard_power_vec]
    )
    schedule_expire_renewed_onboards_vec = schedule_expire_renewed_onboards_full_vec[
        :forecast_lenght
    ]
    schedule_expire_renew_vec = (
        schedule_expire_renewed_known_vec + schedule_expire_renewed_onboards_vec
    )
    return schedule_expire_renew_vec
