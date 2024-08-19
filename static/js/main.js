function searchFilm() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function back() {
    window.history.back();
}

$(document).ready(function () {
    $('#myTable').DataTable({
        paging: true,  // Ativa a paginação
        pageLength: 10,  // Define o número de linhas por página
        info: true,  // Mostra informações de paginação
        searching: false,  // Desativa a barra de pesquisa
        responsive: true,  // Ativa o layout responsivo
        "language": {
          "emptyTable": "Não há itens disponíveis.",
          "paginate": {
            "previous": "Anterior",
            "next": "Próximo"
          },
          "info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
          "lengthMenu": "Mostrar _MENU_ entradas"
        }
    });

});
