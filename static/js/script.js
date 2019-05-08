function send(id, status) {
    var com;
    console.log(status);
    $("#exampleModal").on("shown.bs.modal", function () {
    }).modal('show');
    $('#ok').on('click', function(){
        com = $('#comafclose').val();
        $.ajax({
            url: '/update/' + id,
            data: {
                'id': id,
                'status': status,
                'com' : com,
            },
            success: function(data) {
                $('#downtime-table').bootstrapTable('load', data);
            }
        });
        $("#exampleModal").on("hide.bs.modal", function () {
        }).modal('hide');
    });
    $('#comafclose').val('');
};


function actionsFormatter(value, index, id) {


    if (value == "") {
        return `
              <div class="btn-group">
                <button type="button" class="btn btn-success" onclick="send(${index.id}, 1)">Завершить</button>
                <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" data-toggle="dropdown">
                  <span class="caret"></span>
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="padding:0px;">
                  <button class="dropdown-item btn btn-danger" style="width:100%;" onclick="send(${index.id}, 0)">Отменить простой</button>
                </div>
              </div>
              `;
    }
    return value;
};


function getdata(sort_type = '') {

    $.ajax(
        $('#downtime-table').bootstrapTable({
            url: '/get/',
            columns: [{
                title: 'Номер простоя',
                field: 'number',
                width: '40'
            }, {
                field: 'name',
                title: 'Точка',
                width: '130'

            }, {
                field: 'reasons',
                title: 'Причины',
                width: '130'
            }, {
                field: 'comments',
                title: 'Комментарий'
            }, {
                field: 'startdate',
                title: 'Дата начала',
                width: '190'
            }, {
                field: 'created_by',
                title: 'Открыл',
                width: '190'
            }, {
                field: 'finishdate',
                title: 'Дата окончания',
                formatter: 'actionsFormatter',
                width: '190'
            },
            {
                field: 'com_a_close',
                title: 'Комментарий по закрытию',
            }, {
                field: 'closed_by',
                title: 'Закрыл',
                width: '190'
            }],
            exportDataType: sort_type,
            exportTypes: ['excel', 'csv', 'xml', 'txt', 'doc']
            // avialable also 'json', 'xml', 'png', 'csv', 'txt', 'sql', 'doc', 'excel', 'powerpoint', 'pdf'
        })
    );
};


function rowStyle(row, index) {

    // console.log(row)

    if (row.status == "2" && row.mass_error == true) {
        return {
            classes: 'darkred'
        }
    }
    if (row.status == "0") {
        return {
            classes: 'warning'
        }
    }
    if (row.status == "2") {
        return {
            classes: 'danger'
        }
    }
    return {
        classes: 'success'
    };
};


function change_sort(new_sort_type) {

    $('#downtime-table').bootstrapTable('destroy');
    getdata(new_sort_type);

    console.log(new_sort_type)
    console.log($('#downtime-table').bootstrapTable('getOptions'));
}

$(function() {
    $('#toolbar').find('select').change(function()

        {
            change_sort($(this).val());
        }
    );
});


getdata()

function show_alert() {
    alert('HI!')
}
