function validar_alterar_produto() {
	form = document.forms[0]
	var input = $('.form-control');
	var valid = true;
	var valor = 0;
  	for(var i=0; i < input.length; i++){
     	if (input[i].type == 'text' || input[i].type == 'textarea') {
     		valor += validar_required(input[i].id)
     	}
 		if(input[i].type == 'url') {
 			valor += validar_url(input[i].id)
     	}    	
  	}
  	valor += validar_checked('tamanhos','tamanho', 'Selecione ao menos 1 tamanho!')
  	valor += validar_checked('cores','cor', 'Selecione ao menos 1 cor!')
  	vestuario_invalido = validar_select('select_vestuario','select-vestuario', 'Selecione um tipo')
  	valor += vestuario_invalido
  	if(vestuario_invalido == 0) {
  		valor += validar_select('select_categoria','select-categoria', 'Selecione uma categoria')
  	}
  	if(valor == 0) {
  		form.action = "/dollce/administracao/produto"
  		form.submit()
  	}
}
function validar_select(id, classe, msg) {
	var option = $('.' + classe);
	campo_msg = $('#msg-' + id)
	campo = $('#' + id)
	var selected = 0
	for(var i=0; i < option.length; i++) {
		if(option[i].selected == true){
			selected = 1
		}
	}
	if(selected > 0) {
		campo_msg.text('')
		campo.removeClass('border-error');
		return 0
	} else {
		campo_msg.text(msg);
		campo_msg.addClass('msg-error');
		campo.addClass('border-error');
		return 1
	}
}

function validar_url(id) {
	campo = $('#' + id)
	campo_msg = $('#msg-' + id)
	try {
	    let url = new URL(campo.val())
	    campo_msg.text('')
	    campo.removeClass('border-error');
	    return 0
  	} catch(err) {
      	campo_msg.text("URL inválida. Tente novamente!");
      	campo_msg.addClass('msg-error');
      	campo.addClass('border-error');
  		return 1
  	}
}

function validar_checked(id, classe, msg) {
	var input = $('.' + classe);
	var checked = 0
	campo_msg = $('#msg-' + id)
    for(var i=0; i < input.length; i++) {
    	if(input[i].checked){
    		checked += 1
    	}
    }
    if(checked > 0){
    	campo_msg.text('')
    	return 0
    } else {
    	campo_msg.text(msg);
    	campo_msg.addClass('msg-error');
    	return 1
    }
}

function validar_required(id) {
	campo = $('#' + id)
	campo_msg = $('#msg-' + id)
	if(campo.val().length >= 3){
		campo_msg.text('')
		campo.removeClass('border-error');
		return 0
	}
	else {
		campo_msg.text("Preencha esse campo");
		campo_msg.addClass('msg-error');
		campo.addClass('border-error');
		return 1
	}
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