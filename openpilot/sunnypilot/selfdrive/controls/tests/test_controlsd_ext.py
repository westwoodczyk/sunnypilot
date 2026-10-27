import unittest

from opendbc.car import structs
from openpilot.sunnypilot.selfdrive.controls.controlsd_ext import ControlsExt


class _TorqueLikeTuning:
  def which(self) -> str:
    return "torque"


class _CPStub:
  def __init__(self, steer_control_type):
    self.steerControlType = steer_control_type
    self.lateralTuning = _TorqueLikeTuning()


class _ParamsStub:
  """Fails loudly if the torque override logic is reached at all."""

  def get_bool(self, key: str) -> bool:
    raise AssertionError(f"params must not be read for non-torque cars, got {key}")

  def get(self, key: str, **kwargs) -> str:
    raise AssertionError(f"params must not be read for non-torque cars, got {key}")


def _make_ext(steer_control_type) -> ControlsExt:
  ext = ControlsExt.__new__(ControlsExt)
  ext.CP = _CPStub(steer_control_type)
  ext.params = _ParamsStub()
  return ext


class TestInitializeLateralControl(unittest.TestCase):
  """A torque controller would log a LateralTorqueState, which controlsd cannot publish into
  angleState/curvatureState (capnp type mismatch) and crashes controlsd."""

  def test_angle_car_keeps_angle_controller(self):
    lac = object()
    ext = _make_ext(structs.CarParams.SteerControlType.angle)
    self.assertIs(ControlsExt.initialize_lateral_control(ext, lac, None, 0.01), lac)

  def test_curvature_car_keeps_curvature_controller(self):
    lac = object()
    ext = _make_ext(structs.CarParams.SteerControlType.curvature)
    self.assertIs(ControlsExt.initialize_lateral_control(ext, lac, None, 0.01), lac)
