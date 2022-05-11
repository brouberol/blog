"""
This markdown plugin is in charge of injecting the decoding=async and loading=lazy
attributes on all img nodes.

"""

from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
from markdown.extensions import Extension


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
