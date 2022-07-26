document.addEventListener('DOMContentLoaded', function() {
  if (/profile/.test(window.location.href)) {
    document.querySelector('#show-posts').style.display = 'none';
  }
  document.querySelectorAll('.editing_form').forEach(function(element){
    element.style.display = 'none'
  });
})

function edit_post(actual_content, id, previous_content, edit_form, new_edits, edit_button) {
  var post_id = parseInt(id)
  if (edit_button.innerHTML === "Edit Post") {
    previous_content.style.display = 'none';
    edit_form.style.display = 'block';
    edit_button.innerHTML = "Save Post";
  } else {
    var new_content = new_edits.value;
    previous_content.style.display = 'block';
    edit_form.style.display = 'none';
    edit_button.innerHTML = "Edit Post";
    fetch(`/edit/${post_id}`, {
      method:'POST',
      body: JSON.stringify({
        content: new_content
        })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result)
          actual_content.innerHTML = result["content"];
      }); 
  }
}


function like_post(id, element, user, element2) {
  var int_id = parseInt(id);
  if (element2.innerHTML === "Unlike") {
    fetch(`/likes/${int_id}`, {
    method:'POST',
    body: JSON.stringify({
      action: "unlike"
      })
    })
    .then(response => response.json())
    .then(result => {
        element.innerHTML = result["likers"];
        element2.innerHTML = "Like";
    });
    } else {
      fetch(`/likes/${int_id}`, {
        method:'POST',
        body: JSON.stringify({
          action: "like"
          })
        })
        .then(response => response.json())
        .then(result => {
            element.innerHTML = result["likers"];
            element2.innerHTML = "Unlike";
        });
    } 
}

function show_posts(element){
  if (element.innerHTML === "Show Posts"){
    document.querySelector('#show-posts').style.display = 'block';
    element.innerHTML = "Hide Posts"
  } else {
    document.querySelector('#show-posts').style.display = 'none';
    element.innerHTML = "Show Posts"
  }
}


function follow(element1, element2, profile, user) { 
  if (element1.innerHTML === "Unfollow"){
    fetch(`/follow/${profile}`, {
      method:'POST',
      body: JSON.stringify({
        action: "unfollow"
        })
      })
      .then(response => response.json())
      .then(result => {
          element2.innerHTML = result["followers"];
          element1.innerHTML = "Follow"
      });
  } else {
    fetch(`/follow/${profile}`, {
      method:'POST',
      body: JSON.stringify({
        action: "follow"
        })
      })
      .then(response => response.json())
      .then(result => {
          element2.innerHTML = result["followers"];
          element1.innerHTML = "Unfollow"
      });
  }
}
