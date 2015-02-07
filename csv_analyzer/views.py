# views.py for the django app: csv_analyzer
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from csvanalyzer import CSVSummary, OUTPUT_COLUMNS, DISPLAYABLE_COLUMNS
from django.utils.safestring import mark_safe
import os

FILE_PATH = 'static/'                                        # local dev
# FILE_PATH = '/home/hedson/webapps/tailwind_labs_static/'   # webfaction


def select_file(request):
    if request.method == 'POST': # form has been submitted; process it
            file_choice = request.POST['file_choice']
            return HttpResponseRedirect(reverse('csv_analyzer:analyze', kwargs={'filename': file_choice}))
    else: # form has not been submitted; show form
        return render(request, 'csv_analyzer/select.html')


def analyze(request, filename=None):
    if filename:
        if os.path.isfile(''.join((FILE_PATH, filename))):
            full_path = ''.join((FILE_PATH, filename))
            csv_obj = CSVSummary(full_path)
            # turn the data into a list of lists for use in django template                      
            row_list = []
            for row in csv_obj.output['rows']:
                # convert each row to an ordered list of values for use in django template
                rlist = []
                for col in OUTPUT_COLUMNS:
                    rlist.append(row[col])
                row_list.append(rlist)
            return render(request, 'csv_analyzer/analyze.html', 
                        {   'filename': filename, 
                            'rows': row_list, 
                            'cols': DISPLAYABLE_COLUMNS,
                            'csv_rows': "{:,}".format(csv_obj.csv_row_count),
                            'csv_cols': "{:,}".format(len(row_list))
                        })
        else: # File not found on server
            msg = mark_safe('<span class="text-danger">Error! %s not found on server.</span>' % filename)
    else:
        msg = mark_safe('<span class="text-danger">Error! You must choose a file.</span>')
    # any unexpected case
    return render(request, 'csv_analyzer/analyze.html', {'message': msg})
