import numpy as np
from computation import gdal_utils
from computation.my_simple_calc import RasterInfo

from topocorrection.TopoCorrectionAlgorithm import TopoCorrectionAlgorithm, TopoCorrectionContext


class CosineCTopoCorrectionAlgorithm(TopoCorrectionAlgorithm):
    @staticmethod
    def get_name():
        return "COSINE-C"

    def init(self, ctx: TopoCorrectionContext):
        # todo add validation
        self.luminance_mean = gdal_utils.compute_band_means(ctx.luminance_path)[0]

    def process_band(self, ctx: TopoCorrectionContext, band_idx: int):
        def calculate(**kwargs):
            input_band = kwargs["input"]
            luminance = kwargs["luminance"]

            return input_band * (1 + np.divide(
                self.luminance_mean - luminance,
                self.luminance_mean,
                out=input_band.astype('float32'),
                where=input_band > 5
            ))

        return self.raster_calculate(
            calc_func=calculate,
            raster_infos=[
                RasterInfo("input", ctx.input_layer.source(), band_idx + 1),
                RasterInfo("luminance", ctx.luminance_path, 1),
            ]
        )
