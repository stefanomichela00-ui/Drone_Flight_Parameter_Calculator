
import pytest
from pytest import approx
from project import get_float, calculate_hovering_thrust, calculate_current_consumption, calculate_flight_time  


def test_calculate_hovering_thrust():
    assert calculate_hovering_thrust(1, 4) == 9.81
    assert calculate_hovering_thrust(0.5, 4) == 4.905


def test_calculate_current_consumption():
    T = 10.0
    D = 0.254
    KV = 1000.0
    I0 = 1.0
    TTR = 10.0
    
    assert calculate_current_consumption(T, D, KV, I0, TTR) == approx(105.72, 0.01)

    T = 20.0
    D = 0.3
    KV = 500.0
    I0 = 0.5
    TTR = 12.0
    
    assert calculate_current_consumption(T, D, KV, I0, TTR) == approx(87.76, 0.01)

def test_calculate_flight_time():
    expected_time = (5000 * 0.85 / 1000 / 10.0) * 60
    assert calculate_flight_time(5000, 10.0) == expected_time

    expected_time_high = (10000 * 0.85 / 1000 / 5.0) * 60
    assert calculate_flight_time(10000, 5.0) == expected_time_high