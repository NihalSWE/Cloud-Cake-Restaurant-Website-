import bleach

def sanitize_html(html_content):
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'strong', 'em', 'u', 'strike', 'sub', 'sup', 'ol', 'ul', 'li', 'img', 'span', 'blockquote', 'hr', 'pre', 'code'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title', 'height', 'width'],
        'span': ['style'],
        'p': ['style'],
        'h1': ['style'], 'h2': ['style'], 'h3': ['style'], 'h4': ['style'], 'h5': ['style'], 'h6': ['style']
    }
    return bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attributes)
