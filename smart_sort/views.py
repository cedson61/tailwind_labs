from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import smart_sort.smartsort as ss
import json
from random import shuffle


def ss_page(request):
    # parse the test data string into a list and shuffle it
    temp_list = ss.test_data_string.splitlines()
    shuffle(temp_list)
    shuffled_test_data_string = '\n'.join(temp_list)

    # put the test data into a template context dict
    context = {'test_data': shuffled_test_data_string}

    # render the client demo page, with the shuffled test data
    return render(request, 'smart_sort/sort.html', context)


def ss_api(request):
    # load the json sent by post into a python dictionary
    input_data = json.loads(request.body)
    
    # list comprehension to remove any values that are only whitespace
    cleansed_data = [item for item in input_data['values'] if item.strip()]

    # Build a dictionary with the results of smartSort()
    return_dict = ss.smart_sort(cleansed_data)

    # convert the dictionary to json and return it
    return_value = json.dumps(return_dict)
    return HttpResponse(return_value, content_type='application/json')
