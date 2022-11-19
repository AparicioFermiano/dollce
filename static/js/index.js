function trocar_imagem(id) {
	imagem_destaque = document.getElementById('image_destaque')
	imagem_destaque.src = id.src
}

function buscar_categoria(id_vestuario) {
	$('#select_categoria').empty();
	$.ajax({
		url: "/dollce/administracao/produto",
		type: "GET",
		contentType: 'application/json',
		data: {
			'id_vestuario': id_vestuario
		},
		success: function(response){
			$('#categoria').removeClass('esconder');
			$('#select_categoria').append('<option selected disabled>Selecionar</option>');
			response.forEach(function(e){
                if(e.id_categoria == $('#id_categoria').val()){
                	$('#select_categoria').append('<option class="select-categoria" selected value='+ e.id_categoria +'>' + e.tipo + '</option>');
                } else {
                	$('#select_categoria').append('<option class="select-categoria" value='+ e.id_categoria +'>' + e.tipo + '</option>');
                }
	        });
		},
       	error: function() {
   			alert('Problema ao buscar as categorias');
       }
   	});
}

