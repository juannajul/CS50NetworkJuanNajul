document.addEventListener('DOMContentLoaded', function() {
    //document.querySelector('#edit-post-link').addEventListener('click', () => load_edit_page('edit_post'));
    localStorage.clear();
    const post_link = document.querySelector('#edit-post-link');
    document.querySelectorAll('#edit-post-link').forEach(post_link =>{
    post_link.onclick = function (){
        load_edit_post('edit_post', this.dataset.postid);
    }
    });
});


function load_edit_post(edit_page, post_id) {
    document.querySelector("#edit-modal-post").style.display = 'block';
    console.log(edit_page);
    console.log(post_id);
    localStorage.clear()
    fetch(`/editPost/${post_id}`)
        .then(response => response.json())
        .then(post => {
        // Print email
        console.log(post);
        var post_content = post.content;
        console.log(post_content)
        document.querySelector("#postEditContent").value = `${post_content}`;
        document.querySelector("#postEditContent").focus();
        document.querySelector("#postEditContent").onkeyup = () =>{
            localStorage.setItem('loaded_content', document.querySelector('#postEditContent').value);
            post_content = localStorage.getItem('loaded_content')
        }
        document.querySelector('#cancel-edit-post-link').addEventListener('click', () => {
            localStorage.clear();
            document.querySelector("#edit-modal-post").style.display = 'none';  
        });
        document.querySelector('#edit-content-post-button').addEventListener('click', () => edit_content_post(post_id, post_content)); 
    });
    
}

function edit_content_post(post_id, post_content) {
    fetch(`/editPost/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: document.querySelector("#postEditContent").value = `${post_content}`
        })
      });
      console.log(post_content)
      localStorage.clear()
       let post_new_content = document.querySelector(`[data-contentid = "${post_id}"]`);
       let content = `${post_content}`;
       content = content.replace(/\n/g, "<br />");
       post_new_content.innerHTML  = `<p class="post-content col-12" >${content}</p>`//`${post_content}"|linebreaksbr"`;
      document.querySelector("#edit-modal-post").style.display = 'none'; 
}
//problema al actualizar los posts en el perfil
