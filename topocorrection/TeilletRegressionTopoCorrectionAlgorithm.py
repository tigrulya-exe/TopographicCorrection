from computation import gdal_utils
from computation.my_simple_calc import RasterInfo
from topocorrection.SimpleRegressionTopoCorrectionAlgorithm import SimpleRegressionTopoCorrectionAlgorithm
from topocorrection.TopoCorrectionAlgorithm import TopoCorrectionContext


class TeilletRegressionTopoCorrectionAlgorithm(SimpleRegressionTopoCorrectionAlgorithm):
    @staticmethod
    def get_name():
        return "Teillet regression"

    def init(self, ctx: TopoCorrectionContext):
        self.raster_means = gdal_utils.compute_band_means(ctx.input_layer.source())

    def process_band(self, ctx: TopoCorrectionContext, band_idx: int):
        intercept, slope = self.get_linear_regression_coeffs(ctx, band_idx)

        def calculate(**kwargs):
            input_band = kwargs["input"]
            luminance = kwargs["luminance"]

            return input_band - slope * luminance - intercept + self.raster_means[band_idx]

        return self.raster_calculate(
            calc_func=calculate,
            raster_infos=[
                RasterInfo("input", ctx.input_layer.source(), band_idx + 1),
                RasterInfo("luminance", ctx.luminance_path, 1),
            ]
        )
