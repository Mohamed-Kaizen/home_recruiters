import secrets
import string

from core.settings import settings

chars_string = string.ascii_lowercase + string.digits + string.ascii_uppercase


def slugify(*, value: str) -> str:
    """slugify a string"""

    return (
        value.replace(" ", "-")
        .replace("_", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("@", "")
    )


def random_string(
    *,
    size: int = getattr(settings, "CODE_SIZE", 9),
    chars: str = getattr(settings, "RANDOM_CHARS", chars_string),
) -> str:
    """This function generate random string."""
    return "".join(secrets.choice(chars) for _ in range(size))


def unique_slug(*, title: str, new_slug: str = None) -> str:
    """create unique slug"""

    if new_slug is not None:

        slug = new_slug

    else:

        slug = slugify(value=title)

        new_slug = f"{slug}-{random_string()}"

        return new_slug

    return slug
