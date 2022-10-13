import numpy as np
import pandas as pd
from typing import Callable, Tuple

# --------------------------------------------------------------------------------------
#  QA Multiplier functions
# --------------------------------------------------------------------------------------
def compute_qa_factor(
    fil_plus_rate: float,
    fil_plus_m: float = 10.0,
    duration_m: Callable = None,
    duration: int = None,
) -> float:
    fil_plus_multipler = 1.0 + (fil_plus_m - 1) * fil_plus_rate
    if duration_m is None:
        return fil_plus_multipler
    else:
        return duration_m(duration) * fil_plus_multipler


# --------------------------------------------------------------------------------------
#  Onboardings
# --------------------------------------------------------------------------------------
def forecast_rb_daily_onboardings(
    rb_onboard_power: float, forecast_lenght: int
) -> np.array:
    rb_onboarded_power_vec = np.ones(forecast_lenght) * rb_onboard_power
    return rb_onboarded_power_vec


def forecast_qa_daily_onboardings(
    rb_onboard_power: float,
    fil_plus_rate: float,
    forecast_lenght: int,
    fil_plus_m: float = 10.0,
    duration_m: Callable = None,
    duration: int = None,
) -> np.array:
    # If duration_m is not provided, qa_factor = 1.0 + 9.0 * fil_plus_rate
    qa_factor = compute_qa_factor(fil_plus_rate, fil_plus_m, duration_m, duration)
    qa_onboard_power = qa_factor * rb_onboard_power
    qa_onboarded_power_vec = np.ones(forecast_lenght) * qa_onboard_power
    return qa_onboarded_power_vec


# --------------------------------------------------------------------------------------
#  Renewals
# --------------------------------------------------------------------------------------
def compute_day_rb_renewed_power(
    day_i: int,
    day_scheduled_expire_power_vec: np.array,
    renewal_rate: float,
):
    day_renewed_power = renewal_rate * day_scheduled_expire_power_vec[day_i]
    return day_renewed_power


def compute_day_qa_renewed_power(
    day_i: int,
    day_rb_scheduled_expire_power_vec: np.array,
    renewal_rate: float,
    fil_plus_rate: float,
    fil_plus_m: float = 10.0,
    duration_m: Callable = None,
    duration: int = None,
):
    qa_factor = compute_qa_factor(fil_plus_rate, fil_plus_m, duration_m, duration)
    day_renewed_power = (
        qa_factor * renewal_rate * day_rb_scheduled_expire_power_vec[day_i]
    )
    return day_renewed_power


# --------------------------------------------------------------------------------------
#  Scheduled expirations
# --------------------------------------------------------------------------------------
def compute_day_se_power(
    day_i: int,
    known_scheduled_expire_vec: np.array,
    day_onboard_vec: np.array,
    day_renewed_vec: np.array,
    duration: int,
):
    # Scheduled expirations coming from known active sectors
    if day_i > len(known_scheduled_expire_vec) - 1:
        known_day_se_power = 0.0
    else:
        known_day_se_power = known_scheduled_expire_vec[day_i]
    # Scheduled expirations coming from modeled sectors
    if day_i - duration >= 0:
        model_day_se_power = (
            day_onboard_vec[day_i - duration] + day_renewed_vec[day_i - duration]
        )
    else:
        model_day_se_power = 0.0
    # Total scheduled expirations
    day_se_power = known_day_se_power + model_day_se_power
    return day_se_power


# --------------------------------------------------------------------------------------
#  Power stats
# --------------------------------------------------------------------------------------
def forecast_power_stats(
    rb_power_zero: float,
    qa_power_zero: float,
    rb_onboard_power: float,
    rb_known_scheduled_expire_vec: np.array,
    qa_known_scheduled_expire_vec: np.array,
    renewal_rate: float,
    fil_plus_rate: float,
    duration: int,
    forecast_lenght: int,
    fil_plus_m: float = 10.0,
    duration_m: Callable = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Forecast onboards
    day_rb_onboarded_power = forecast_rb_daily_onboardings(
        rb_onboard_power, forecast_lenght
    )
    total_rb_onboarded_power = day_rb_onboarded_power.cumsum()
    day_qa_onboarded_power = forecast_qa_daily_onboardings(
        rb_onboard_power,
        fil_plus_rate,
        forecast_lenght,
        fil_plus_m,
        duration_m,
        duration,
    )
    total_qa_onboarded_power = day_qa_onboarded_power.cumsum()
    # Initialize scheduled expirations and renewals
    day_rb_scheduled_expire_power = np.zeros(forecast_lenght)
    day_rb_renewed_power = np.zeros(forecast_lenght)
    day_qa_scheduled_expire_power = np.zeros(forecast_lenght)
    day_qa_renewed_power = np.zeros(forecast_lenght)
    # Run loop to forecast daily scheduled expirations and renewals
    for day_i in range(forecast_lenght):
        # Raw-power stats
        day_rb_scheduled_expire_power[day_i] = compute_day_se_power(
            day_i,
            rb_known_scheduled_expire_vec,
            day_rb_onboarded_power,
            day_rb_renewed_power,
            duration,
        )
        day_rb_renewed_power[day_i] = compute_day_rb_renewed_power(
            day_i, day_rb_scheduled_expire_power, renewal_rate
        )
        # Quality-adjusted stats
        day_qa_scheduled_expire_power[day_i] = compute_day_se_power(
            day_i,
            qa_known_scheduled_expire_vec,
            day_qa_onboarded_power,
            day_qa_renewed_power,
            duration,
        )
        day_qa_renewed_power[day_i] = compute_day_qa_renewed_power(
            day_i,
            day_rb_scheduled_expire_power,
            renewal_rate,
            fil_plus_rate,
            fil_plus_m,
            duration_m,
            duration,
        )
    # Compute total scheduled expirations and renewals
    total_rb_scheduled_expire_power = day_rb_scheduled_expire_power.cumsum()
    total_rb_renewed_power = day_rb_renewed_power.cumsum()
    total_qa_scheduled_expire_power = day_qa_scheduled_expire_power.cumsum()
    total_qa_renewed_power = day_qa_renewed_power.cumsum()
    # Total RB power
    rb_power_zero_vec = np.ones(forecast_lenght) * rb_power_zero
    rb_total_power = (
        rb_power_zero_vec
        + total_rb_onboarded_power
        - total_rb_scheduled_expire_power
        + total_rb_renewed_power
    )
    # Total QA power
    qa_power_zero_vec = np.ones(forecast_lenght) * qa_power_zero
    qa_total_power = (
        qa_power_zero_vec
        + total_qa_onboarded_power
        - total_qa_scheduled_expire_power
        + total_qa_renewed_power
    )
    # Build DataFrames
    rb_df = pd.DataFrame(
        {
            "forecasting_step": np.arange(forecast_lenght),
            "onboarded_power": day_rb_onboarded_power,
            "cum_onboarded_power": total_rb_onboarded_power,
            "expire_scheduled_power": day_rb_scheduled_expire_power,
            "cum_expire_scheduled_power": total_rb_scheduled_expire_power,
            "renewed_power": day_rb_renewed_power,
            "cum_renewed_power": total_rb_renewed_power,
            "total_power": rb_total_power,
        }
    )
    rb_df["power_type"] = "raw-byte"
    qa_df = pd.DataFrame(
        {
            "forecasting_step": np.arange(forecast_lenght),
            "onboarded_power": day_qa_onboarded_power,
            "cum_onboarded_power": total_qa_onboarded_power,
            "expire_scheduled_power": day_qa_scheduled_expire_power,
            "cum_expire_scheduled_power": total_qa_scheduled_expire_power,
            "renewed_power": day_qa_renewed_power,
            "cum_renewed_power": total_qa_renewed_power,
            "total_power": qa_total_power,
        }
    )
    qa_df["power_type"] = "quality-adjusted"
    return rb_df, qa_df
