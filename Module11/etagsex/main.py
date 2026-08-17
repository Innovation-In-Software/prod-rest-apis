from fastapi import FastAPI, Header, HTTPException, Response

app = FastAPI()

# our "database": one product with a version number
product = {"name": "Coffee Mug", "price": 12.99, "version": 1}


@app.get("/product")
def get_product(response: Response, if_none_match: str = Header(default=None)):
    etag = str(product["version"])

    # Job 1 — caching: client already has this version, send nothing back
    if if_none_match == etag:
        return Response(status_code=304)

    response.headers["ETag"] = etag
    return product


@app.put("/product")
def update_product(price: float, if_match: str = Header(...)):
    etag = str(product["version"])

    # Job 2 — concurrency: version changed, reject the save
    if if_match != etag:
        raise HTTPException(412, "Product changed; fetch the latest and retry")

    product["price"] = price
    product["version"] += 1
    return product