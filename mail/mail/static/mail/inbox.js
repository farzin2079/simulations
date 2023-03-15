document.addEventListener('DOMContentLoaded', function() {
    
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  document.querySelector('#compose-form').addEventListener('submit', sendmail);

  
  // By default, load the inbox
  load_mailbox('inbox');
  
  function compose_email() {
    
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    
  }
  
  function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><ul id="list"></ul>`;
    
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      
      emails.forEach(email => {
        const button = document.createElement('button')
        const li = document.createElement('div')
        const list = document.querySelector('#list')
        button.className = 'email-button'
        button.dataset.email = `${email.id}`
        button.innerHTML = `from: ${email.sender} | subject: ${email.subject} | time: ${email.timestamp} `
        
        if (email.read == false){
          li.className = 'email'
        }
        else{
          li.className = 'email read'
        }
        
        li.appendChild(button)
        list.append(li)
        document.querySelectorAll('.email-button').forEach(function(button) {
          button.onclick = function(){
            fetch(`/emails/${button.dataset.email}`)
            .then(response => response.json())
            .then(mail => {
              // show singel email
              const div = document.querySelector('#emails-view')
              
              const demo = document.createElement('div')
              //sender field
              const h3 = document.createElement('h3')
              // timestamp field
              const h6 = document.createElement('h6')
              // body field
              const p = document.createElement('p')
              // subject field
              const h4 = document.createElement('h4')
              
              // archive button
              const archive = document.createElement('button')
              archive.id = 'archive'
              archive.dataset.id = mail.id
              archive.innerHTML = 'archive'
              archive.className = 'btn btn-sm btn-outline-primary'
              if (mail.archived){
                archive.className = 'btn btn-sm btn-outline-primary active'
              }
              // replay button
              const replay = document.createElement('button')
              replay.id = 'replay'
              replay.dataset.id = mail.id
              replay.innerHTML = 'replay'
              replay.className = 'btn btn-sm btn-outline-primary'
              
              h3.innerHTML = `send from: ${mail.sender}`
              h6.innerHTML = `${mail.timestamp}`
              p.innerHTML = `${mail.body}`
              h4.innerHTML = `subject: ${mail.subject}`
              
              // style selector
              h3.id = 'sender'
              h4.id = 'subject'
              h6.id = 'timestamp'
              p.id = 'body'
              
              // change read to true
              fetch(`/emails/${mail.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  read: true
                })
              })            
              demo.append( h3, h4, h6, replay, p, archive)
              div.innerHTML = demo.innerHTML

              document.querySelector('#archive').addEventListener('click', archived);
              document.querySelector('#replay').addEventListener('click', replayAction);
            })
            return false
          }})
        });
        
      
      return false;
    })
    }
  })

function sendmail() {
  
    fetch("/emails", {
        method : "POST",
        body: JSON.stringify({
          recipients: document.querySelector("#compose-recipients").value,
          subject: document.querySelector("#compose-subject").value,
          body: document.querySelector("#compose-body").value
        })
      })
      .then(response => response.json())
      .then(result => {
        if (result.message == 'Email sent successfully.')
        {
          alert(result.message)
        return load_mailbox('send')
        }
        else
        {
          alert('somting wrong try again')
          return compose_email();
        }
      });
      return false
    }

function archived(){
  const button = document.querySelector('#archive')
  const archive = button.dataset.id
   
  fetch(`/emails/${archive}`)
  .then(response => response.json())
  .then(mail => {

    if (mail.archived){
      fetch(`/emails/${mail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
    })
   button.className = 'btn btn-sm btn-outline-primary'
  }
  else{
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
    button.className = 'btn btn-sm btn-outline-primary active'
  }
})
  }



function replayAction(){
  const replay = document.querySelector('#replay').dataset.id
  fetch(`emails/${replay}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `${email.timestamp} <<${email.sender}>> wrote:${email.body}`;
  })
  return false
}