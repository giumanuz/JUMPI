import os


def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result


# To learn the detailed concept of "span" in the following codes, visit: https://aka.ms/spans
def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False


def analyze_layout():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # If analyzing a local document, remove the comment markers (#) at the beginning of these 8 lines.
    # Delete or comment out the part of "Analyze a document at a URL" above.
    # Replace <path to your sample file>  with your actual file path.
    path_to_sample_document = "<path to your sample file>"
    with open(path_to_sample_document, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream"
        )
    result: AnalyzeResult = poller.result()
    # print(result.as_dict())
    return result.as_dict()


    # [START extract_layout]
    # Analyze whether the document contains handwritten content.
    if result.styles and any([style.is_handwritten for style in result.styles]):
        print("Document contains handwritten content")
    else:
        print("Document does not contain handwritten content")

    # Analyze pages.
    # To learn the detailed concept of "bounding polygon" in the following content, visit: https://aka.ms/bounding-region
    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
        print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        # Analyze lines.
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                print(
                    f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                    f"within bounding polygon '{line.polygon}'"
                )

                # Analyze words.
                for word in words:
                    print(f"......Word '{word.content}' has a confidence of {word.confidence}")

        # Analyze selection marks.
        if page.selection_marks:
            for selection_mark in page.selection_marks:
                print(
                    f"Selection mark is '{selection_mark.state}' within bounding polygon "
                    f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
                )
        # Note that selection marks returned from begin_analyze_document(model_id="prebuilt-layout") do not return the text associated with the checkbox.
        # For the API to return this information, build a custom model to analyze the checkbox and its text. For detailed steps, visit: https://aka.ms/train-your-custom-model

    # Analyze tables.
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
            if table.bounding_regions:
                for region in table.bounding_regions:
                    print(f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}")
            # Analyze cells.
            for cell in table.cells:
                print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
                if cell.bounding_regions:
                    for region in cell.bounding_regions:
                        print(f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'")

    # Analyze figures.
    # To learn the detailed concept of "figures" in the following content, visit: https://aka.ms/figures
    if result.figures:
        for figures_idx,figures in enumerate(result.figures):
            print(f"Figure # {figures_idx} has the following spans:{figures.spans}")
            for region in figures.bounding_regions:
                print(f"Figure # {figures_idx} location on page:{region.page_number} is within bounding polygon '{region.polygon}'")

    print("----------------------------------------")
    # [END extract_layout]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        analyze_layout()
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
