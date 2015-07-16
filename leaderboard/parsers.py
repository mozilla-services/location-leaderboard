import StringIO

from rest_framework.parsers import JSONParser, ParseError

from leaderboard.utils.compression import gzip_decompress


class GzipJSONParser(JSONParser):
    """A parser that decompressed a gzip stream

    For this parser to kick in, the client must provide a value
    for the ``Content-Encoding`` header. The only accepted value is
    ``gzip``. Any other value is ignored.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        headers = parser_context['request'].META.get('headers', {})
        if headers.get('Content-Encoding', '') == 'gzip':
            raw_content = stream.read()

            try:
                uncompressed_content = gzip_decompress(raw_content)
            except IOError, e:
                raise ParseError('gzip error - {}'.format(e))

            stream = StringIO.StringIO(uncompressed_content)

        return super(GzipJSONParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)
