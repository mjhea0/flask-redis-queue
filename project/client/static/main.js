// custom javascript

$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('.btn').on('click', function() {
  $.ajax({
    url: '/tasks',
    data: { type: $(this).data('type') },
    method: 'POST'
  })
  .done((res) => {
    getStatus(res.data.task_id)
  })
  .fail((err) => {
    console.log(err)
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`
    $('#tasks').prepend(html);
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}
