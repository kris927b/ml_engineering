"""Module building the FastAPI endpoints"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv

from app.chain_prompts import chain_of_prompts, single_prompt
from app.utils import convert_string_to_json

app = FastAPI(title="Adverts")


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/process_advert")
async def process_advert(
    image: UploadFile = File(...), heatmap: UploadFile = File(...)
):
    load_dotenv()
    # Convert uploaded files to appropriate formats (e.g., base64 or PIL Image)
    image_data = await image.read()
    heatmap_data = await heatmap.read()

    # Step 1: Process A
    process_a1_output, process_a2_output = chain_of_prompts(image_data, heatmap_data)

    # Step 2: Process B
    process_b_output = single_prompt(image_data)

    # Step 3: Process C
    # final_output = process_c(process_a1_output, process_a2_output, process_b_output)

    return {
        "a1": convert_string_to_json(process_a1_output),
        "a2": convert_string_to_json(process_a2_output),
        "b": convert_string_to_json(process_b_output),
    }  # json.loads(f"[{process_a1_output}, {process_a2_output}]")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
