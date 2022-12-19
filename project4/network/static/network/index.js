document.addEventListener('DOMContentLoaded', () =>{

    document.querySelectorAll('#delete').forEach(del => {
        del.onclick = ()=>{ 
                fetch(`delete/${del.dataset.id}`,{
                    method: 'POST'
                })
                .then(res => res.json())
                .then(massage =>{
                    if (massage.massage == 'deleted'){
                        document.querySelector(`#div-${del.dataset.id}`).style.display = 'none' 
                    }
                    else{
                        alert('Pleas Retry')
                    }
                })
            }
        })


    document.querySelectorAll('#edit').forEach(edit => {
        edit.onclick = ()=>{ 

            const div = document.createElement('div')
            const form = document.createElement('form')
            const input = document.createElement('input')
            const textarea = document.createElement('textarea')
            const submit = document.createElement('button')

            form.action = `/edit/${edit.dataset.id}`
            form.method = 'post'
            form.className = 'mb-3'

            input.type = 'text'
            input.name = 'title'
            input.placeholder = 'title'
            input.className = 'form-control'
            
            textarea.placeholder = 'post text'
            textarea.name = 'body'
            textarea.className = 'form-control'

            submit.type = 'submit'
            submit.innerHTML = 'edit'
            submit.className = 'btn btn-primary'

            form.append(input, textarea, submit)
            div.append(form)
            document.querySelector(`#div-${edit.dataset.id}`).innerHTML = div.innerHTML;
        }
    })

     document.querySelectorAll('#like').forEach(like => {
        
        like.onclick = ()=>{
            fetch(`/like/${like.dataset.id}`,{
                method: 'POST'
            })
            .then(res => res.json())
            .then(massage =>{
                const likes = document.querySelector(`#like-${like.dataset.id}`)
                var count = likes.innerHTML

            if (massage.massage == 'like'){
                like.className = 'btn btn-outline-danger active'
                like.innerHTML = 'unlike'
                count++
                likes.innerHTML = count
            }
            else{
                like.className = 'btn btn-outline-danger'
                like.innerHTML = 'like'
                count--
                likes.innerHTML = count
            }
        })
        }
     });

    document.querySelector('#follow').onclick = ()=>{
        const id = document.querySelector('#follow').dataset.user
        fetch(`/follow/${id}`,{
            method : "POST"
        })
        .then(response => response.json())
        .then(massage =>{
            var count = document.querySelector('#count').innerHTML
           if (massage.massage == 'followed'){
            document.querySelector('#follow').className = 'btn btn-outline-dark active'
            count++
            document.querySelector('#count').innerHTML = count;
           }
           else{
            document.querySelector('#follow').className = 'btn btn-outline-dark'
            count--
            document.querySelector('#count').innerHTML = count;
           }
        })
    }

})

