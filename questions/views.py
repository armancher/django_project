from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages

from questions.forms import QuestionForm,AnswerForm,SearchForm ,TagForm
from questions.models import Question, Answer, Tag


# Create your views here.
def question_detail_view(request, question_id):
    question=get_object_or_404(Question,id=question_id)
    answers = Answer.objects.filter(question=question)
    form= AnswerForm()
    context={
        'question' :question ,
        'form' : form ,  
        'answers': answers ,      
    }
    return render(request,'question/question_detail_view.html',context)
    


def question_list_view(request):
    questions=Question.objects.all()
    return render(request,'question/question_list_view.html',{'questions': questions})


def question_update_view(request, question_id):
    question=get_object_or_404(Question,id=question_id)
    if request.method=='POST':
        form=QuestionForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            return redirect('questions:question_list')
    else:
        form=QuestionForm(instance=question)
    return render(request,'question/question_form.html',{'form':form ,'question_id':question_id})

def question_delete_view(request, question_id):
    question=get_object_or_404(Question,id=question_id)
    question.delete()
    return redirect('questions:question_list')

def question_upvote_view(request, question_id):
    question=get_object_or_404(Question,id=question_id)
    if not question.upvoters.filter(id=request.user.id).exists() :
  
        if question.downvoters.filter(id=request.user.id).exists() :
            question.downvoters.remove(request.user)
            
        question.upvoters.add(request.user)
        question.save()
    return redirect('questions:question_detail', question_id=question_id)


def question_downvote_view(request, question_id):
    question=get_object_or_404(Question,id=question_id)
    if not question.downvoters.filter(id=request.user.id).exists():
        
        if question.upvoters.filter(id=request.user.id).exists() :
            question.upvoters.remove(request.user)
        
        question.downvoters.add(request.user)
        question.save()
    return redirect('questions:question_detail', question_id=question_id)


def question_create_view(request):
    if request.method=='POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()
            return redirect('questions:question_list')
    else:
        form=QuestionForm()
    context={
            'form': form ,
        }
    return render(request,'question/question_form.html',context=context)

    


def question_search_view(request):
    questions=[]
    if request.method == 'POST' :
        form=SearchForm(request.POST)
        if form.is_valid():
            questions=Question.objects.filter(title=form.cleaned_data.get('query'))
         
        
    else:
        form=SearchForm()
    context={
            'form': form ,
            'questions':  questions ,
        }
    return render(request,'question/question_form.html',context=context)

    
        


def answer_create_view(request, question_id):  
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('questions:question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    
    return render(request, 'question/question_detail_view.html', {'form': form ,'question':question })



def answer_update_view(request, answer_id): 
    answer = get_object_or_404(Answer, id=answer_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            
            return redirect('questions:question_detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context={
        'form': form,
        'answer_id': answer_id ,
        'question' : answer.question ,
        'answer': Answer.objects.filter(question=answer.question) ,
        'update': True ,
        
        
    }
    return render(request, 'question/question_detail_view.html',context)




def answer_delete_view(request, answer_id):
    answer=get_object_or_404(Answer,id=answer_id)

    answer.delete()
    return redirect('questions:question_list')


def answer_upvote_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if not answer.upvoters.filter(id=request.user.id).exists():
        if answer.downvoters.filter(id=request.user.id).exists():
            answer.downvoters.remove(request.user)
        answer.upvoters.add(request.user)
        answer.save()
    
    return redirect('questions:question_detail', question_id=answer.question.id)


def answer_downvote_view(request, answer_id): 
    answer = get_object_or_404(Answer, id=answer_id)
    if not answer.downvoters.filter(id=request.user.id).exists():
        if answer.upvoters.filter(id=request.user.id).exists():
            answer.upvoters.remove(request.user)
        
        
        answer.downvoters.add(request.user)
        answer.save()
    
    
    return redirect('questions:question_detail', question_id=answer.question.id)


def tag_list_view(request):
    tags = Tag.objects.all()
    context = {
        'tags' : tags ,
    }
    return render(request , 'tag/tag_list_view.html',context)


def tag_create_view(request): 
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('users:home')
    else :
        form = TagForm()
        context = {
            'form' : form
        }
        return render(request , 'tag/create_tag_form.html', context)
   
