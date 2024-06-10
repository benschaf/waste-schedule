// Comment edit functionality
let editButtons = document.getElementsByClassName("edit-button");
for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        const commentFieldId = e.target.dataset.commentFieldId;
        const commentField = document.getElementById(commentFieldId);
        const actionUrl = e.target.dataset.actionUrl;
        const currentText = commentField.innerText;
        const csrfToken = e.target.dataset.csrfToken;
        // I wonder if this makes my token vulnerable ...
        commentField.innerHTML = `
                    <form method="POST" action="${actionUrl}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <input type="textarea" class="form-control" name="body" value="${currentText}">
                        <input type="submit" value="Edit Comment" class="btn btn-link text-muted p-0">
                    </form>`;
    });
}