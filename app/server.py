"""Module building the FastAPI endpoints"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv

from app.chain_prompts import (
    chain_of_prompts,
    single_prompt,
    summarization_prompt,
)

app = FastAPI(title="Adverts")


@app.get("/")
async def redirect_root_to_docs():
    """Redirect to docs when accessing root

    Returns:
        RedirectResponse: Redirect to docs page
    """
    return RedirectResponse("/docs")


@app.post("/process_advert")
async def process_advert(
    image: UploadFile = File(...), heatmap: UploadFile = File(...)
) -> dict:
    """Process an advert and the heatmap from neurons.

    Args:
        image (UploadFile, optional): Image of an advert. Defaults to File(...).
        heatmap (UploadFile, optional): Heatmap of an advert. Defaults to File(...).

    Returns:
        dict: Dictionary with four keys: ad_description, ad_purpose, saliency_description, cognitive_description.
    """

    load_dotenv()
    # Convert uploaded files to appropriate formats (e.g., base64 or PIL Image)
    image_data = await image.read()
    heatmap_data = await heatmap.read()

    # Step 1: Process A
    process_a1_output, process_a2_output = chain_of_prompts(image_data, heatmap_data)

    # Step 2: Process B
    process_b_output = single_prompt(image_data)

    # Step 3: Process C
    final_output = summarization_prompt(
        process_a1_output, process_a2_output, process_b_output
    )

    return final_output.dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
