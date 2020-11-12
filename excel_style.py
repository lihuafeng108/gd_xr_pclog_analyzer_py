
class excel_style:

    def __init__(self):
        pass

    def get_highest_head_style(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(13)
        src_format.set_bold(True)
        src_format.set_border(2)
        src_format.set_align('center')
        src_format.set_align('vcenter')
        src_format.set_bg_color('#CCFF66')
        return src_format

    def get_title_style(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(12)
        src_format.set_bold(True)
        src_format.set_border(2)
        src_format.set_align('center')
        src_format.set_align('vcenter')
        src_format.set_bg_color('#009999')
        return src_format

    def get_text_style_light(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(12)
        src_format.set_border(1)
        src_format.set_align('right')
        src_format.set_align('vcenter')
        src_format.set_bg_color('#F0F0F0')
        src_format.set_text_wrap()  # 自动换行
        return src_format

    def get_text_style_dark(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(12)
        src_format.set_border(1)
        src_format.set_align('right')
        src_format.set_align('vcenter')
        src_format.set_bg_color('#66CC66')
        src_format.set_text_wrap()  # 自动换行
        return src_format

    def get_text_style_pink(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(12)
        src_format.set_border(1)
        src_format.set_align('right')
        src_format.set_align('vcenter')
        src_format.set_bg_color('pink')
        src_format.set_text_wrap()  # 自动换行
        return src_format

    def get_text_style_left_dark(self, src_format):
        src_format.set_font('宋体')
        src_format.set_size(12)
        src_format.set_border(1)
        src_format.set_align('left')
        src_format.set_align('vcenter')
        src_format.set_bg_color('#66CC66')
        src_format.set_text_wrap()  # 自动换行
        return src_format