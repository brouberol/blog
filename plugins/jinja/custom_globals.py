def responsive_image(unsized_image_path, suffix_to_size, max_width, alt):
    """Generate a responsive <img> element.

    See https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images

    Example:
        <img
            srcset="elva-fairy-480w.jpg 480w, elva-fairy-800w.jpg 800w"
            sizes="(max-width: 600px) 480px, 800px"
            src="elva-fairy-800w.jpg"
            alt="Elva dressed as a fairy"
        />

    """
    srcset = []
    max_size, max_size_image_path = 0, None
    unsized_image_path = unsized_image_path.strip()

    for suffix, size in suffix_to_size.items():
        # Inject the suffix before the extension in the provided path
        sized_image_path = (
            ".".join(unsized_image_path.split(".")[:-1])
            + f"-{suffix}."
            + unsized_image_path.split(".")[-1]
        )
        srcset.append(f"{sized_image_path} {size}w")
        if size > max_size:
            max_size = size
            max_size_image_path = sized_image_path

    sizes = sorted(suffix_to_size.values())
    return "\n".join(
        [
            "<img",
            f'src="{max_size_image_path}"',
            f'srcset="{", ".join(srcset)}"',
            f'sizes="(max-width: {max_width}px) {sizes[0]}w, {sizes[1]}w"',
            f'alt="{alt}"',
            f'title="{alt}"',
            "/>",
        ]
    )
