__version__ = '0.1.1'
__author__ = 'Danielfiks'
__doc__ = '''The purpose of this file is to generate a pdf with a provided json file'''

from reportlab.platypus import Frame, Paragraph, Image, Table, Spacer, KeepInFrame
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import yaml
import json

global logo
PURPOSE_MAX_LENGTH: int = 800 # The purpose field has a max length.
LOCALES_FILEPATH: str = "./locales/"

STANDARD_TBL_STYLE = [('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                      ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
                      ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                      ('LEFTPADDING', (0, 0), (-1, -1), 4),
                      ('RIGHTPADDING', (0, 0), (-1, -1), 4)]




def load_locales(chosen_locales):
    with open(LOCALES_FILEPATH + chosen_locales + ".yaml", "r") as yaml_file:
        return yaml.safe_load(yaml_file)

def load_form_data(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def get_attachments(invoice) -> list[Paragraph]:
    data = []

    for item in invoice["attachments"]:
        file_raw = str(item.get("file"))
        invoice_from_raw = str(item.get("invoice_from"))
        invoice_info_raw = str(item.get("invoice_info"))
        date_raw = str(item.get("date"))
        invoice_sum_raw = str(item.get("invoice_sum"))

        row = [Paragraph(file_raw),
               Paragraph(invoice_from_raw),
               Paragraph(invoice_info_raw),
               Paragraph(date_raw),
               Paragraph(invoice_sum_raw)]

        data.append(row)

    return data

def select_language(selected_language):
    if not isinstance(selected_language, str):
        raise TypeError(f"{selected_language} must be a string")

    match selected_language:
        case "en" | "nb" | "nn":
            return load_locales(selected_language)
        case _:
            return load_locales("nb")


def generate_pdf(filename, language, input_logo_filepath="./assets/spillhusetLogo.png",
                 data_filepath="./assets/data.json") -> None:

    provided_data = load_form_data(data_filepath)

    if not isinstance(filename, str):
        raise TypeError(f"{filename} must be a string")

    if not isinstance(input_logo_filepath, str):
        raise TypeError(f"{input_logo_filepath} must be a string")





    doc = Canvas(filename, pagesize=A4)

###################################### Styles ###############
    styles = getSampleStyleSheet()
    base_font = 'Helvetica'
    label_style = ParagraphStyle(name='Label',
                                fontName=base_font,
                                fontSize=10,
                                leading=12,
                                alignment=TA_LEFT)

    note_style = ParagraphStyle(name='Small', fontName=base_font, fontSize=9,
                               leading=11, alignment=TA_LEFT, textColor=colors.grey)

    heading1_center = ParagraphStyle(name= 'Heading1_CENTER',
                                     parent=styles['Heading1'],
                                     alignement=TA_CENTER,
                                     fontSize=13)



    normal = styles['Normal']
    title = styles['Title']


    # A flowable located in the first frame.
    def document_header_flowable(logo_filepath) -> list[Table]:
        logo_image = Image(logo_filepath, width=150, height=75)
        header = Paragraph(f"<b> {locale['document']['title'].upper()} </b>", title)
        data = [[logo_image, header]]

        tbl = Table(data, hAlign='CENTER', colWidths=[55 * mm, None])
        tbl.setStyle([('BOX', (0, 0), (-1, -1), 0.5, colors.white),
                      ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                      ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                      ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                      ('LEFTPADDING', (0, 0), (-1, -1), 4),
                      ('RIGHTPADDING', (0, 0), (-1, -1), 4)])

        return tbl


    # Frame 2
    def personal_field() -> Table:
        name_label = Paragraph(f"<b>{locale['personal_field']['name']}</b>", normal)
        phone_label = Paragraph(f"<b>{locale['personal_field']['phone']}</b>", normal)
        refund_date_label = Paragraph(f"<b>{locale['personal_field']['refund_date']}</b>", normal)
        date_label = Paragraph(f"<b>{locale['personal_field']['date']}</b>", normal)
        account_number_label = Paragraph(f"<b>{locale['personal_field']['account_number']}</b>", normal)

        name_data = [[name_label, provided_data['name']]]

        data = [[phone_label, provided_data['phone'], date_label, provided_data['date']],
                [refund_date_label, provided_data['refund_date'], account_number_label, provided_data['account_number']]]


        tbl = [Table(name_data, hAlign='CENTER', colWidths=[60 * mm, None],
                     style=STANDARD_TBL_STYLE),

               Table(data, hAlign='CENTER', colWidths=[60 * mm, None, None, None],
                     style=STANDARD_TBL_STYLE)
               ]

        return tbl

    def purpose_field() -> list[Spacer | Paragraph | Table]:
        if len(provided_data['purpose']) > PURPOSE_MAX_LENGTH:
            raise ValueError(f"Input is too long. Maximum allowed length is {PURPOSE_MAX_LENGTH} characters.")


        data = Paragraph(provided_data['purpose'], normal)

        flowable = [Spacer(1, 2 * mm),
                    Paragraph(f"<b>{locale['personal_field']['purpose']}</b>", normal),
                    Spacer(1, 1 * mm),
                    Table([[data]], rowHeights=90, colWidths=498.24,
                          style=[('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                                 ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                 ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                 ('LEFTPADDING', (0, 0), (-1, -1), 4),
                                 ('RIGHTPADDING', (0, 0), (-1, -1), 4)])]

        return flowable

    #Frame 3
    def third_flowable():
        frame_heading = Paragraph(
            f"<b> {locale['attachments_section']['heading'].upper()} </b>",
            heading1_center)
        file_label = Paragraph(
            f"<b>{locale['attachments_section']['attachment']}</b>", normal)
        billing_label = Paragraph(
            f"<b>{locale['attachments_section']['invoice_from']}</b>", normal)
        receipt_info_label = Paragraph(
            f"<b>{locale['attachments_section']['invoice_info']}</b>", normal)
        receipt_date_label = Paragraph(
            f"<b>{locale['attachments_section']['invoice_date']}</b>", normal)
        sum_label = Paragraph(
            f"<b>{locale['attachments_section']['invoice_sum']}</b>", normal)
        sum_expenses_label = Paragraph(
            f"<b>{locale['attachments_section']['expenses_sum']}</b>",
            label_style)

        tbl_heading = [[file_label, billing_label, receipt_info_label, receipt_date_label, sum_label]]

        # Get the list
        attachments_data = get_attachments(provided_data)
        attachments_tbl_width = [80, 70, None, 70, 80]

        tbl_header = Table(tbl_heading, hAlign='LEFT', colWidths= attachments_tbl_width,
                           style = [('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('SPAN', (0, 3), (3, 3)),
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                                    ('RIGHTPADDING', (0, 0), (-1, -1), 4)])

        tbl = Table(attachments_data, hAlign='CENTER', colWidths=attachments_tbl_width,
                     style=[('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 4),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 4)
                            ])

##################### SUM Field ###############################################

        sum_data = Paragraph(f"<b>{provided_data['expenses_sum']} kr</b>", normal)
        total_sum = [[sum_expenses_label, '', '', '', sum_data]]

        tbl_sum = Table(total_sum, style=[('BOX', (0, 0), (-1, -1), 1.5, colors.black),
                                          ('SPAN', (0, 3), (3, 3)),
                                          ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                          ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                          ('LEFTPADDING', (0, 0), (-1, -1), 4),
                                          ('RIGHTPADDING', (0, 0), (-1, -1), 4)])


################### NOTE ###########################
        note_data = str(provided_data["note"] + " " + str(locale['notice']['default_note']) + ".")

        note_sec = [Spacer(1,5),
                    Paragraph(f"<b>{locale['notice']['heading']}</b>", label_style),
                    Paragraph(note_data, note_style)]

        return [frame_heading,tbl_header, tbl] + [tbl_sum] + note_sec


    x1 = 42.52
    width = 510.24

    # height: 842 , old: 687.40
    frame1 = Frame(x1, 719, width, 93) # No touch
    frame2 = Frame(x1, 529, width, 190) # No touch
    frame3 = Frame(x1, 30, width, 499)

    frame1.add(first_flowable(input_logo_filepath), doc)
    frame2.addFromList(personal_info(), doc)

    try:
        frame2.addFromList(purpose_field(), doc)
    except ValueError:
        print(f"Input is too long. Maximum allowed length is {PURPOSE_MAX_LENGTH} characters.")


    content = third_flowable()

    box = KeepInFrame(
        maxWidth=frame3.width,           # typically match the frame width
        maxHeight=frame3.height,         # here: 150
        content=content,
        mode="shrink"

    )

def main() -> None:
    generate_pdf("bilagForUtleggsoppgjør.pdf", "nb",
                 "./assets/spillhusetLogo.png", "./assets/data.json")


if __name__ == "__main__":
    main()