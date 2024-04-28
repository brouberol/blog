"""
This markdown plugin is in charge of injecting the decoding=async and loading=lazy
attributes on all img nodes.

"""

from markdown.extensions import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor


class AsyncDecodedImgInlineProcessor(ImageInlineProcessor):
    def handleMatch(self, m, data):
        el, start, index = super().handleMatch(m, data)
        el.set("decoding", "async")
        el.set("loading", "lazy")
        return el, start, index


class AsyncDecodedImgExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            AsyncDecodedImgInlineProcessor(IMAGE_LINK_RE, md), "img", 175
        )
