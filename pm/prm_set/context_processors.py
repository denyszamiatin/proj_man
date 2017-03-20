
def projects_proc(request):
    domain = '{}://{}'.format(request.scheme, request.META['HTTP_HOST'])
    return {'PORTAL_URL': domain}