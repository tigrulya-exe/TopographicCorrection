import processing

from algorithms.TopoCorrectionAlgorithm import TopoCorrectionAlgorithm, TopoCorrectionContext


class ScsTopoCorrectionAlgorithm(TopoCorrectionAlgorithm):
    @staticmethod
    def get_name():
        return "[old] SCS"

    def process_band(self, ctx: TopoCorrectionContext, band_idx: int):
        result = processing.run(
            'gdal:rastercalculator',
            {
                # create layer from luminance_layer
                'INPUT_A': ctx.luminance_path,
                'BAND_A': 1,
                'INPUT_B': ctx.input_layer,
                'BAND_B': band_idx + 1,
                'INPUT_C': ctx.slope_rad_path,
                'BAND_C': 1,
                'FORMULA': f"{ctx.sza_cosine()}*cos(C)*{self.safe_divide('B', 'A')}",
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'NO_DATA': 0
            },
            feedback=ctx.qgis_feedback,
            context=ctx.qgis_context
        )
        return result['OUTPUT']
