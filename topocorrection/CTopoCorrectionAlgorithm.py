import numpy as np

from topocorrection.SimpleRegressionTopoCorrectionAlgorithm import SimpleRegressionTopoCorrectionAlgorithm
from topocorrection.TopoCorrectionAlgorithm import TopoCorrectionContext
from computation.my_simple_calc import RasterInfo


class CTopoCorrectionAlgorithm(SimpleRegressionTopoCorrectionAlgorithm):
    @staticmethod
    def get_name():
        return "C-correction"

    def process_band(self, ctx: TopoCorrectionContext, band_idx: int):
        c = self.calculate_c(ctx, band_idx)

        def calculate(**kwargs):
            input_band = kwargs["input"]
            luminance = kwargs["luminance"]

            denominator = luminance + c
            return input_band * np.divide(
                ctx.sza_cosine() + c,
                denominator,
                out=input_band.astype('float32'),
                where=np.logical_and(denominator > 0, input_band > 5)
            )

        return self.raster_calculate(
            calc_func=calculate,
            raster_infos=[
                RasterInfo("input", ctx.input_layer.source(), band_idx + 1),
                RasterInfo("luminance", ctx.luminance_path, 1),
            ]
        )

    def calculate_c(self, ctx: TopoCorrectionContext, band_idx: int) -> float:
        intercept, slope = self.get_linear_regression_coeffs(ctx, band_idx)
        return intercept / slope
