document.addEventListener('DOMContentLoaded', function() {
    
  // Edit functionality
  document.querySelectorAll('.edit-btn').forEach(button => {
      button.addEventListener('click', function() {
          const postId = this.dataset.postId;
          const postCard = document.querySelector(`#post-${postId}`);
          const contentElement = postCard.querySelector('.post-content');
          const currentContent = contentElement.textContent;
          
          // Replace content with textarea
          contentElement.innerHTML = `
              <textarea class="form-control edit-textarea" rows="3" maxlength="280">${currentContent}</textarea>
              <button class="btn btn-success btn-sm mt-2 save-btn" data-post-id="${postId}">Save</button>
              <button class="btn btn-secondary btn-sm mt-2 cancel-btn">Cancel</button>
          `;
          
          // Hide edit button
          this.style.display = 'none';
          
          // Add event listener to save button
          const saveBtn = postCard.querySelector('.save-btn');
          saveBtn.addEventListener('click', function() {
              const newContent = postCard.querySelector('.edit-textarea').value;
              
              // Send PUT request to server
              fetch(`/edit/${postId}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      content: newContent
                  })
              })
              .then(response => response.json())
              .then(data => {
                  if (data.message) {
                      // Update content
                      contentElement.textContent = data.content;
                      // Show edit button again
                      button.style.display = 'inline-block';
                  } else {
                      alert('Error: ' + data.error);
                  }
              })
              .catch(error => {
                  console.error('Error:', error);
                  alert('An error occurred');
              });
          });
          
          // Add event listener to cancel button
          const cancelBtn = postCard.querySelector('.cancel-btn');
          cancelBtn.addEventListener('click', function() {
              contentElement.textContent = currentContent;
              button.style.display = 'inline-block';
          });
      });
  });

  // Like functionality
  document.querySelectorAll('.like-btn').forEach(button => {
      button.addEventListener('click', function() {
          const postId = this.dataset.postId;
          const likeIcon = this.querySelector('.like-icon');
          const likeCount = this.querySelector('.like-count');
          
          // Send POST request to toggle like
          fetch(`/like/${postId}`, {
              method: 'POST'
          })
          .then(response => response.json())
          .then(data => {
              // Update UI
              if (data.liked) {
                  likeIcon.textContent = '❤️';
                  this.dataset.liked = 'true';
              } else {
                  likeIcon.textContent = '🤍';
                  this.dataset.liked = 'false';
              }
              likeCount.textContent = data.like_count;
          })
          .catch(error => {
              console.error('Error:', error);
          });
      });
  });
});