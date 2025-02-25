import contextlib
from pathlib import Path
from typing import Any

import boto3

from misc.hasher import get_b64encoded_digest


@contextlib.contextmanager
def prepare_put_object(s3, bucket_name: str, exist_objs: list[dict[str, Any]]):
    try:
        yield s3
    finally:
        if exist_objs:
            s3.delete_objects(
                Bucket=bucket_name,
                Delete={
                    "Objects": [
                        {
                            "Key": obj["Key"],
                        }
                    for obj in exist_objs]
                }
            )


def upload_template(template_path: Path, bucket_name: str) -> str:
    digest = get_b64encoded_digest(template_path.read_bytes()).removesuffix("=")
    filename = f"{digest}-{template_path.name}"

    s3 = boto3.client("s3")

    objs = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    if len(list(filter(lambda obj: obj["Key"] == filename, objs))) > 0:
        # Skip upload
        return filename

    with prepare_put_object(s3, bucket_name, objs) as s3:
        s3.put_object(
            ACL="private",
            Body=template_path.read_bytes(),
            Bucket=bucket_name,
            CacheControl="max-age=31536000",
            ContentType="text/yaml",
            Key=filename,
        )

    return filename
