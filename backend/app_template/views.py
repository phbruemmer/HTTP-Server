"""
Example view:

def home(request):                      # view function
    args = {
        'username': 'test',             # arguments dictionary for the HTML file
    }
                                        # returns an HTTP response with the prepared HTML file data
    return render.render(request, 'main/HTML_files/home.html', args) 
"""

# Create your views here
