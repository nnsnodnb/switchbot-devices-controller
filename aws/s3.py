import contextlib
from pathlib import Path
from typing import Any

import boto3

from github.repos import get_latest_commit_hash
from misc.hasher import get_b64encoded_digest


class AlreadyExistObjectError(Exception):
    s3_key: str

    def __init__(self, s3_key: str):
        self.s3_key = s3_key
        super().__init__(f"Object already exists: {s3_key}")


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
                        for obj in exist_objs
                    ]
                },
            )


def _upload_object(object_path: Path, bucket_name: str, dest_filename: str, folder: str, content_type: str) -> str:
    s3_key = f"{folder}/{dest_filename}"

    s3 = boto3.client("s3")

    objs = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder).get("Contents", [])
    if len(list(filter(lambda obj: obj["Key"] == s3_key, objs))) > 0:
        # Skip upload
        raise AlreadyExistObjectError(s3_key) from None

    with prepare_put_object(s3, bucket_name, objs) as s3:
        s3.put_object(
            ACL="private",
            Body=object_path.read_bytes(),
            Bucket=bucket_name,
            CacheControl="max-age=31536000",
            ContentType=content_type,
            Key=s3_key,
        )

    return s3_key


def upload_source_code(source_code_path: Path, bucket_name: str, token: str, repo: str, branch: str = "main") -> str:
    sha = get_latest_commit_hash(token=token, repo=repo, branch=branch)
    dest_filename = f"{sha}-{source_code_path.name}"

    filename = _upload_object(
        object_path=source_code_path,
        bucket_name=bucket_name,
        dest_filename=dest_filename,
        folder="sources",
        content_type="application/zip",
    )

    return filename


def upload_template(template_path: Path, bucket_name: str) -> str:
    digest = get_b64encoded_digest(template_path.read_bytes()).removesuffix("=")
    dest_filename = f"{digest}-{template_path.name}"

    filename = _upload_object(
        object_path=template_path,
        bucket_name=bucket_name,
        dest_filename=dest_filename,
        folder="templates",
        content_type="text/yaml",
    )

    return filename
