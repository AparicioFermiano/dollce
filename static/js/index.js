function trocar_imagem(id) {
	imagem_destaque = document.getElementById('image_destaque')
	imagem_destaque.src = id.src
}

function selecionar_todos(id, classe) {
    if(id.checked) {
        $('.' + classe).each(function() {
            this.checked = true;               
        });
    }else{
        $('.' + classe).each(function() {
            this.checked = false;                       
        });         
    };
}

function buscar_categoria(id_vestuario) {
	$('#select_categoria').empty();
	$.ajax({
		url: "/gestor/produto",
		type: "GET",
		contentType: 'application/json',
		data: {
			'id_vestuario': id_vestuario
		},
		success: function(response){
			$('#categoria').removeClass('esconder');
			$('#select_categoria').append('<option selected disabled>Selecionar</option>');
			response.forEach(function(e){
                $('#select_categoria').append('<option value='+ e.id_categoria +'>' + e.tipo + '</option>');
	        });
		},
       	error: function() {
   			alert('Problema ao buscar as categorias');
       }
   	});
}

function ajax_alterar_produto() {
	form = document.forms[0]
	form.submit()
}
