//===== Upload Image ==========
function readURL(input) {
    var fileTypes = ['jpg', 'jpeg', 'png', 'svg', 'webp', 'pdf'];  //acceptable file types
    if (input.files && input.files[0]) {
        var extension = input.files[0].name.split('.').pop().toLowerCase(),  //file extension from input file
            isSuccess = fileTypes.includes(extension);  //is extension in acceptable types
        if (isSuccess) { //yes
            var reader = new FileReader();
            reader.onload = function (e) {
                $(input).parents('.property_img').find(".clear_document").removeClass('d-none')
                $(input).parents('.property_img').find(".imgBase64").val(e.target.result.split(',')[1])
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $(input).parents('.property_img').find(".docErr").removeClass('d-none').fadeIn();
            setTimeout(function() {
                $(input).parents('.property_img').find(".docErr").fadeOut('slow');
                    }, 9000);
        }
    }else{
        $(input).parents('.property_img').find(".clear_document").addClass('d-none')
    }
}
odoo.define('property_website_ee.property_website_rpc', function(require) {
        var odoo = require('web.ajax');

    $(document).ready(function(e){
    	
    	if ((window.location.href.indexOf('/lease-properties') > 0) || (window.location.href.indexOf('/search_properties') > 0)){
            // bedroom slide js
            $("#bead_slider_range").slider({
                range: true,
                animate: true,
                step: 1,
                min: 1,
                max: 5,
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                values: [$('#min_bead_range_id').val(), $('#max_bead_range_id').val()],
                slide: function(event, ui) {
                    $("#bead_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                    $('#min_bead_range_id').val(ui.values[0]);
                    $('#max_bead_range_id').val(ui.values[1]);
                }
            });
            $("#bead_amount").val("" + $("#bead_slider_range").slider("values", 0) + " - " + $("#bead_slider_range").slider("values", 1));
            var $bead_amount = $("#bead_amount").val();
            $('#bead_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
            $('#bead_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

            //  bathroom slide js
            $("#bath_slider_range").slider({
                range: true,
                animate: true,
                step: 1,
                min: 1,
                max: 5,
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                values: [$('#min_bath_range_id').val(), $('#max_bath_range_id').val()],
                slide: function(event, ui) {
                    $("#bath_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                    $('#min_bath_range_id').val(ui.values[0]);
                    $('#max_bath_range_id').val(ui.values[1]);
                }
            });
            $("#bath_amount").val("" + $("#bath_slider_range").slider("values", 0) + " - " + $("#bath_slider_range").slider("values", 1));
            var $bath_amount = $("#bath_amount").val();
            $('#bath_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
            $('#bath_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

            // Price list slide js
            odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {
                $("#price_slider_range").slider({
                    range: true,
                    animate: true,
                    step: 500,
                    min: data['min_value'],
                    max: data['max_value'],
                    heterogeneity: ['50/50000'],
                    format: {
                        format: '##.0',
                        locale: 'de'
                    },
                    dimension: '',
                    values: [data['min_value'], data['max_value']],
                    slide: function(event, ui) {
                        $("#price_slider").val("$" + ui.values[0] + "- $" + ui.values[1]);
                        $('#min_price_range_id').val(ui.values[0]);
                        $('#max_price_range_id').val(ui.values[1]);
                    }
                });
                $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));
                $(".min_range_class").val(data['min_value'])
                $(".max_range_class").val(data['max_value'])
                var $price_slider = $("#price_slider").val();
                $('#price_slider_range a').first().html('<label><span class="fa fa-chevron-left"></span></label>');
                $('#price_slider_range a').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');
            });
        } 
   	 
	   	$('.check_property').change(function(){
	   		var total_selected_property_type_ids = [];
	   		$('.check_property:checked').each(function(){
	               var selected_id =$(this).data('property_type_id')
	               total_selected_property_type_ids.push(selected_id);
	   		});
	   		$('.selected_property_types').val(total_selected_property_type_ids)
	   	});
   	
   	
	    $(".heart").on("click", function() {
	    	$(this).toggleClass("is-active");
	    });

		// Lift card and show stats on Mouseover
		$('#property-card').hover(function(){
				$(this).addClass('animate');
				$('div.carouselNext, div.carouselPrev').addClass('visible');
			 }, function(){
				$(this).removeClass('animate');
				$('div.carouselNext, div.carouselPrev').removeClass('visible');
		});
    	
        $(document).on('click', '.navbar a', function(e){
            $(this).each( function() {
                $(this).parent().removeClass('active');
            });
            $(this).parent().addClass('active');
        })


        //code for click on navbar in responsive view
        $(document).on('click', '.nav.sidebar-nav li .is-closed', function(e){
            if (this['id'] == 'user_account_logout'){
                $(document).find("ul.nav.sidebar-nav li a").addClass('is-open');
            }
            if (this['id'] != 'user_account_logout'){
                $('.hidden-md.hidden-lg.toggled ul.nav.sidebar-nav li a').removeClass('active');
                $(document).find("#wrapper").removeClass('toggled');
                $('#wrapper .overlay').css('display', 'none');
            }
        });
        $(document).on('click', '.nav.sidebar-nav li .is-open', function(e){
            if (this['id'] =='user_account_logout'){
                $(document).find("ul.nav.sidebar-nav li a").addClass('is-open');
            }
            if (this['id'] !='user_account_logout'){
                $('.hidden-md.hidden-lg.toggled ul.nav.sidebar-nav li a').removeClass('active');
                $(document).find("#wrapper").removeClass('toggled');
                $('#wrapper .overlay').css('display', 'none');
            }
        });

        $(document).on('click', '.hero-text', function(e){
            e.preventDefault();
            $('html, body').animate({
                scrollTop: $('.rest').offset().top - 50
            }, 1000);

        });

       // create lead from sales page
        $(document).on('click', '#submit_sale_form', function(e){
        	$("#display_success_msg").css('display', 'none');
            $('#saleForm').addClass('was-validated');
        	if ($('#saleForm')[0].checkValidity() === false) {
        		e.preventDefault();
        		e.stopPropagation();
            	return false;
        	}else{
        		odoo.jsonRpc("/contactus/create_lead", 'call', {
                    'contact_name' : $("input[name='first_name']").val() +' '+$("input[name='last_name']").val(),
                    'phone' : $("input[name='phone']").val(),
                    'email_from' : $("input[name='email_from']").val(),
                    'address' : $("input[name='address']").val(),
                    'city' : $("input[name='city']").val(),
                    'zip' : $("input[name='zip']").val(),
                    'country_id' : $("select[name='country_id']").val(),
                    'value_from' : "Sales page",
                }).then(function() {
                    $('#saleForm')[0].reset();
                    $('#saleForm').removeClass('was-validated');
                    $("#display_success_msg").css('display', 'block');
                });
        	}
        });

        // Request Type(Request book or upload document)
        $("#request_to_book").prop("checked", true);
        $(".upload_document_panel").addClass('d-none');
        $("#token_number").val('')
        $(".request_type").off('click').on("click",function(){
            $("#token_number").val('')
            $(".crm_lead_id").val('')
            $('.contact_info_panel input').val('');
            $('.contact_info_panel textarea').val('');
            $(".all_document_panel").show();
//            $("#residential").prop("checked", false);
//            $("#corporate").prop("checked", false);
            $("#request_upload_documnet_book").prop("checked", true);
            $("#request_upload_documnet_book").trigger('click');
            $(".rent_panel").removeClass('d-none');
            $(".corporate_panel").removeClass('d-none');
            $(".corporate_panel").addClass('d-none');
            var request_type = $(this).val();
            if( request_type == 'upload_document'){
                $(".contact_info_panel").addClass('d-none');
                $(".contact_info_panel input").removeAttr('required');
                $('.contact_info_panel textarea').removeAttr('required');
                $(".rent_panel").addClass('d-none');
                $(".residentail_panel").addClass('d-none');
                $(".upload_document_panel").removeClass('d-none');
                //$(".upload_document_panel input").attr({'required': ''});
                $(".request_upload_documnet_panel").hide();
            }else{
                $(".contact_info_panel").removeClass('d-none');
                $(".contact_info_panel input").attr({'required': ''});
                $('.contact_info_panel textarea').attr({'required': ''});
                $("#residential").prop("checked", true);
                $(".residentail_panel").removeClass('d-none');
                $(".rent_panel").removeClass('d-none')
                $(".upload_document_panel").addClass('d-none');
               // $(".upload_document_panel input").removeAttr('required');
                $(".request_upload_documnet_panel").show()
            }
        })
        
        //Request Upload Document
        if($('#request_upload_documnet_book').prop("checked") == true){
            $("#request_upload_document_panel").show();
//            $("#residential").prop("checked", true);
//            $("#residentail_panel input").attr({'required': ''});
            $("#residential").trigger('click');
        }
        else{
            $("#request_upload_document_panel").hide();
            $("#residential").prop("checked", true);
            $("#corporate").prop("checked", false);
           // $("#residentail_panel input").removeAttr('required');
           // $("#corporate_panel input").removeAttr('required');
        }
        $("#request_upload_documnet_book").off('click').on('click', function(){
            if($(this).prop("checked") == true){
                $("#request_upload_document_panel").show();
                //$("#residential").prop("checked", true);
                //$("#corporate").prop("checked", false);
                //$("#residentail_panel input").attr({'required': ''});
                //$("#corporate input").removeAttr('required');
               // $("#residential").trigger('click');
            }
            else{
                $("#request_upload_document_panel").hide();
                $("#residentail_panel input").val('');
                $("#corporate input").val('');
              //  $("#residential").prop("checked", true);
//                $("#residentail_panel input").removeAttr('required');
//                $("#corporate").prop("checked", false);
//                $("#corporate input").removeAttr('required');
              //  $("#residential").trigger('click');
            }
        });
        
        // Click residential or corporate radio.
        $('.rent_type').off('click').on("click",function(){
            var rent_name = $(this).val();
            if(rent_name == 'residential'){
                $("#residentail_panel").removeClass('d-none');
                //$("#residentail_panel input").attr({'required': ''});
                $("#corporate_panel").addClass('d-none');
               // $("#corporate_panel input").removeAttr('required');
                $("#corporate_panel").find('input').val('');
                $("#corporate_panel").find(".clear_document").addClass('d-none');
            }else{
                $("#residentail_panel").addClass('d-none');
                //$("#residentail_panel input").removeAttr('required');
                $("#residentail_panel").find('input').val('');
                $("#residentail_panel").find(".clear_document").addClass('d-none');
                $("#corporate_panel").removeClass('d-none');
                //$("#corporate_panel input").attr({'required': ''})
            }
        });
        $(".clear_document").off("click").on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            $(this).parents('.property_img').find("input").val('')
            $(this).addClass('d-none')
        });
        $(".serach_incomplete_document").off("click").on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            var token_number = $("#token_number").val();
           // if(token_number){
                odoo.jsonRpc("/contactus/get_create_lead", 'call', {
                    'token_number': token_number,
                }).then(function(lead_result) {
                    $(".all_document_panel").show();
                    $(".crm_lead_id").val('')
                    if(lead_result){
                        console.log("pppppp",lead_result.id, $(".crm_lead_id"))
                        $(".crm_lead_id").val(lead_result.id);
                        if(lead_result.rent_type == 'residential'){
                            $("#request_upload_document_panel").show();
                            $("#residential").trigger('click');
                            $("button.rent_panel").removeClass('d-none');
                            $(".all_document_panel").hide()
                            _.each(lead_result.incomplete_document_list, function(document_list){
                                $("#resd_" + document_list).show();
                            })
                        }else if(lead_result.rent_type == 'corporate'){
                            $("#request_upload_document_panel").show();
                            $("#corporate").trigger('click');
                            $("button.rent_panel").removeClass('d-none');
                            $(".all_document_panel").hide()
                            _.each(lead_result.incomplete_document_list, function(document_list){
                                $("#corp_" + document_list).show();
                            })
                        }
                    }else{
                        $("#request_upload_document_panel").hide();
                        $("#residential").prop("checked", true);
                        $("#residential").trigger('click');
                        if(! $("button.rent_panel").hasClass('d-none')){
                            $("button.rent_panel").addClass('d-none')
                        }
                        $("#display_invalid_token").css('display', 'block');
                        setTimeout(function(){
                            $("#display_invalid_token").css('display', 'none');
                        },5000)
                    }
                });
           // }
        });
    // create lead from perticular property page
        $(document).on('click', '#send_property_id', function(e){
        	$("#display_success_msg").css('display', 'none');
        	$('#selectedpropertyForm').addClass('was-validated');
        	 console.log("$('#selectedpropertyForm')[0].checkValidity() ",$('#selectedpropertyForm')[0].checkValidity() )
        	if ($('#selectedpropertyForm')[0].checkValidity() === false) {
        		e.preventDefault();
        		e.stopPropagation();
            	return false;
        	}else{
        	    var rent_type = $("input[name='rent_type']:checked").val();
        	    var crm_lead_id = $(".crm_lead_id").val()
        	    var request_type = $("input[name='request_type']:checked").val();
        	    var token_number = $("#token_number").val();
        	    var residential_dict = {}
        	    var corporate_dict = {}
        	    if(rent_type == 'corporate'){
        	        var civil_id = $("#civil_id").val();
        	        var passport_copy = $("#passport_copy").val();
        	        var company_licence = $("#company_licence").val();
        	        var company_registration = $("#company_registration").val();
        	        var articale_of_asociation = $("#articale_of_asociation").val();
        	        var annual_company_income = $("#annual_company_income").val();
        	        corporate_dict = {
        	            'civil_id': civil_id,
        	            'passport_copy': passport_copy,
        	            'company_licence': company_licence,
        	            'company_registration': company_registration,
        	            'articale_of_asociation': articale_of_asociation,
        	            'annual_company_income': annual_company_income
        	        }
        	    }else{
        	        var civil_id = $("#r_civil_id").val();
                    var passport_copy = $("#r_passport_copy").val();
                    var work_permit = $("#r_work_permit").val();
                    var salary_certificate = $("#r_salary_certificate").val();
                    var marriage_certificate = $("#r_marriage_certificate").val();
                    var annual_income = $("#r_annual_income").val();
                    residential_dict = {
                        'civil_id': civil_id,
                        'passport_copy': passport_copy,
                        'work_permit': work_permit,
                        'salary_certificate': salary_certificate,
                        'marriage_certificate': marriage_certificate,
                        'annual_income': annual_income
                    }
        	    }
	        	odoo.jsonRpc("/contactus/create_lead", 'call', {
	                'contact_name' : $("input[name='first_name']").val() +' '+ $("input[name='last_name']").val(),
	                'phone' : $("input[name='phone']").val(),
	                'email_from' : $("input[name='email_from']").val(),
	                'telType' : $("select[name='telType']").val(),
	                'telTime' : $("select[name='telTime']").val(),
	                'msg' : $("textarea[name='msg']").val(),
	                'asset': $("input[name='asset']").val(),
	                'value_from' : "Property page",
        	        'rent_type': rent_type,
        	        'request_type': request_type,
        	        'residential_dict': residential_dict,
        	        'corporate_dict': corporate_dict,
        	        'token_number': token_number,
        	        'crm_lead_id': crm_lead_id
	            }).then(function() {
	                $('#selectedpropertyForm')[0].reset();
	                $('#selectedpropertyForm').removeClass('was-validated');
	                $("#display_success_msg").css('display', 'block');
	                setTimeout(function(){
                        $("#display_success_msg").css('display', 'none');
                    },5000)
	                $("#request_upload_document_panel").hide();
	                $("#residential").prop("checked", false);
                    $("#residential").trigger('click');
                    $(".crm_lead_id").val('');
                    if(crm_lead_id){
                        if(! $("button.rent_panel").hasClass('d-none')){
                            $("button.rent_panel").addClass('d-none')
                        }
                    }
	            });
        	}
        });

        $(document).on('click', '.listing-save,.listing-saved-data', function(e){
            var fav_checked = false
            var self = $(this)
        	if ($(this).hasClass('listing-save')){
        		fav_checked = true
            }
            odoo.jsonRpc("/update_fav_property", 'call', {
                'fav_checked': fav_checked,
                'fav_property': $(this).data('lease_id')
            }).then(function(data) {
            	var parent_div =self.parent()
            	if (fav_checked){
            		parent_div.find('.listing-saved-data').css('display', 'block');
                	parent_div.find('.listing-save').css('display', 'none');
            	}else{
            		parent_div.find('.listing-save').css('display', 'block');
                	parent_div.find('.listing-saved-data').css('display', 'none');
            	}
                $('#view_all_asset_sale_saved').html('Saved (' + data +')')
            });
        });
        
//        if (window.location.href.indexOf('/properties/') > 0) {
//        	var list_places = []
//        	initialize()
//        	$('#table-map-near-by .chkbox:checked').each(function(){
//                 list_places.push(this.id);
//            });
//            showMap(list_places)
//        }

        if (window.location.pathname == '/' || window.location.pathname == '/page/homepage'){
        	//set price on the slider dynamically
            odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {

                //code for rent
                $(".form_filter_rent .home_page_filter_price #amount").val("$" + data['min_value'] + " - $" + data['max_value']);
                $('.form_filter_rent .home_page_filter_price #min_property_range_id').val(data['min_value']);
                $('.form_filter_rent .home_page_filter_price #max_property_range_id').val(data['max_value']);
                $(".form_filter_rent .home_page_filter_price #slider_range").slider({
                    range: true,
                    animate: true,
                    step: 500,
                    min: data['min_value'],
                    max: data['max_value'],
                    heterogeneity: ['50/50000'],
                    format: {
                        format: '##.0',
                        locale: 'de'
                    },
                    dimension: '',
                    scale: [0, '|', 50, '|', '100', '|', 250, '|', 500],
                    values: [data['min_value'], data['max_value']],
                    slide: function(event, ui) {
                        $(".form_filter_rent .home_page_filter_price #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
                        $(".form_filter_rent .home_page_filter_price #min_property_range_id").val(ui.values[0]);
                        $(".form_filter_rent .home_page_filter_price #max_property_range_id").val(ui.values[1]);
                    }
                });

                $(".form_filter_rent .home_page_filter_price #amount").val("$" + $(".form_filter_rent .home_page_filter_price #slider_range").slider("values", 0) + " - $" + $(".form_filter_rent .home_page_filter_price #slider_range").slider("values", 1));
                var $amount = $(".form_filter_rent .home_page_filter_price #amount").val();
                $('.form_filter_rent .home_page_filter_price #slider_range a').html('<label><span class="fa fa-chevron-left"></span></label>');
                $('.form_filter_rent .home_page_filter_price #slider_range a').next().html('<label><span class="fa fa-chevron-right"></span></label>');
            });

            // bedroom slide js
            $("#bead_slider_range").slider({
                range: true,
                animate: true,
                step: 1,
                min: 1,
                max: 5,
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                values: [$('#min_bead_range_id').val(), $('#max_bead_range_id').val()],
                slide: function(event, ui) {
                    $("#bead_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                    $('#min_bead_range_id').val(ui.values[0]);
                    $('#max_bead_range_id').val(ui.values[1]);
                }
            });
            $("#bead_amount").val("" + $("#bead_slider_range").slider("values", 0) + " - " + $("#bead_slider_range").slider("values", 1));
            var $bead_amount = $("#bead_amount").val();
            $('#bead_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
            $('#bead_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

            //  bathroom slide js
            $("#bath_slider_range").slider({
                range: true,
                animate: true,
                step: 1,
                min: 1,
                max: 5,
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                values: [$('#min_bath_range_id').val(), $('#max_bath_range_id').val()],
                slide: function(event, ui) {
                    $("#bath_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                    $('#min_bath_range_id').val(ui.values[0]);
                    $('#max_bath_range_id').val(ui.values[1]);
                }
            });
            $("#bath_amount").val("" + $("#bath_slider_range").slider("values", 0) + " - " + $("#bath_slider_range").slider("values", 1));
            var $bath_amount = $("#bath_amount").val();
            $('#bath_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
            $('#bath_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

            // Price list slide js
            odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {
                $("#price_slider_range").slider({
                    range: true,
                    animate: true,
                    step: 500,
                    min: 0,
                    max: data['max_value'],
                    heterogeneity: ['50/50000'],
                    format: {
                        format: '##.0',
                        locale: 'de'
                    },
                    dimension: '',
                    values: [$('#min_price_range_id').val(), $('#max_price_range_id').val()],
                    slide: function(event, ui) {
                        $("#price_slider").val("$" + ui.values[0] + "- $" + ui.values[1]);
                        $('#min_price_range_id').val(ui.values[0]);
                        $('#max_price_range_id').val(ui.values[1]);
                    }
                });
                $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));
                $(".min_range_class").val(data['min_value'])
                $(".max_range_class").val(data['max_value'])
                var $price_slider = $("#price_slider").val();
                $('#price_slider_range a').first().html('<label><span class="fa fa-chevron-left"></span></label>');
                $('#price_slider_range a').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');
            });
        }

        //code for hover and click eveent in sales and rent page property type dropdown
        $(document).on('mouseover', '.dropdown-submenu', function(e){
            $(this).find(".dropdown-menu").attr('style', 'display: block;');

            $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
            $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
        });

        $(document).on('mouseleave', '.dropdown-submenu', function(e){
            if ($(this).find(".dropdown-menu").hasClass('active')){
                $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
                $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
            }
            else{
                $(this).find(".fa.fa-caret-left").attr('style', 'display: none');
                $(this).find(".fa.fa-caret-down").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
                $(this).find(".dropdown-menu").attr('style', 'display: none;');
            }
        });

        $(document).on('click', '.dropdown-submenu', function(e){
            var dorpdown_menu = $(this).children(".dropdown-menu");
            if ($(this).children(".dropdown-menu").hasClass('active')){
                $(this).children(".dropdown-menu").attr('style', 'display: none');
                $(this).children(".dropdown-menu").removeClass('active');
                $(this).find(".fa.fa-caret-left").attr('style', 'display: none');
                $(this).find(".fa.fa-caret-down").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
            }
            else{
                $(this).children(".dropdown-menu").attr('style', 'display: block');
                $(this).children(".dropdown-menu").addClass('active');
                $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
                $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
            }
        });

    //    $("#menu-toggle").click(function(e) {
        $(document).on('click', '#menu-toggle', function(e){
            e.preventDefault();
            $("#wrapper").toggleClass("active");
        });

        if ($(window).width() <= 992) {
            $('.arrow-slidebar').children().children("i").addClass('fa-chevron-right');
           }
           else{
           $('.arrow-slidebar').children().children("i").addClass('fa-chevron-left');
           }
            $(document).on('click', '.social_share_property', function(e){
        });

    //    $('#datetimepicker8').datepicker();
        $(document).bind('click', '.date_maintenance', function(e){
            $('#datetimepicker8').datepicker();
        });

        $(document).on('click', '.maintenane_type_class', function(e){
            $(this).parent('#inputTelType').find('.maintenane_type_class').removeClass('active')
            $(this).addClass('active')
        });

        // create Maintanance from perticular property page
        $(document).on('click', '#submit_maintanance', function(e){
            $('#MaintanancepropertyForm').validator('validate');
            if ($('#MaintanancepropertyForm').find('.has-error:visible').size() > 0) return;
            odoo.jsonRpc("/create_maintanance", 'call', {
                /*'type_id': $('#MaintanancepropertyForm #inputTelType .maintenane_type_class.active').data('type_id'),*/
                'type_id': $('#MaintanancepropertyForm #inputTelType .maintenane_type_class:selected').data('type_id'),
                'date': $('.date_maintenance').val(),
                'description': $('#MaintanancepropertyForm #inputMsg').val(),
                'property_id': $('#MaintanancepropertyForm').data('property_id'),
                'renters_fault': $('#renters_fault').is( ':checked' ),
            }).then(function() {
                $('#MaintanancepropertyForm')[0].reset();
                $("#MaintanancepropertyForm #display_success_msg").css('display', 'block');
            });
        });


    });
});
