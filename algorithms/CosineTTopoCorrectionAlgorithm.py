import processing

from algorithms.TopoCorrectionAlgorithm import TopoCorrectionAlgorithm, TopoCorrectionContext


class CosineTTopoCorrectionAlgorithm(TopoCorrectionAlgorithm):
    @staticmethod
    def get_name():
        return "[old] COSINE-T"

    def process_band(self, ctx: TopoCorrectionContext, band_idx: int):
        result = processing.run(
            'gdal:rastercalculator',
            {
                'INPUT_A': ctx.luminance_path,
                'BAND_A': 1,
                'INPUT_B': ctx.input_layer,
                'BAND_B': band_idx + 1,
                'FORMULA': f"{ctx.sza_cosine()} * {self.safe_divide('B', 'A')}",
                'OUTPUT': 'TEMPORARY_OUTPUT',
            },
            feedback=ctx.qgis_feedback,
            context=ctx.qgis_context
        )
        return result['OUTPUT']
