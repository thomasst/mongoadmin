def globals(request):
    return {
        'show_disconnect': bool(request.session.get('mongoconnection'))
    }
