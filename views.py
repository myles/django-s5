from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from models import Presentation

def list(request):
	presentations = Presentation.objects.all()
	
	return render_to_response('presentations/presentation_list.html', { 'presentations': presentations }, context_instance=RequestContext(request))

def detail(request, slug, topic):
	presentation = Presentation.objects.get(slug=slug)
	slides = presentation.slide_set.all()
	
	return render_to_response('presentations/presentation_detail.html', { 'object': presentation, 'slides': slides }, context_instance=RequestContext(request))
