((function(){var a,b,c;a=function(a){return $.ajax({type:"get",url:"/usps/zip_lookup/",data:{zip:a},success:function(a){$("form#ovr #home_zip_code").val(a.zip);$("form#ovr #home_city").val(a.city);return $("form#ovr #home_state_id").val(a.state)},error:function(a){}})};c=function(){var a,b,c,d;b=$("#pre_first_name").val();c=$("#pre_last_name").val();a=$("#pre_email_address").val();d=$("#pre_zip_code");$("#first_name").val(b);$("#last_name").val(c);$("#email_address").val(a);$("#home_zip_code").val(d);$("#state_form").hide();return $("#registration_form").show()};b=function(){var a,b,d;a="";d="";b={};b["'home_zip_code'"]=$("#pre_zip_code").val();b["'lang'"]=$("#lang_id").val();return $.ajax({url:a+d,data:b,type:"get",success:function(a){var b,d,e,f,g,h,i,j,k;if(a.party_list){h=a.party_list;b=$("select#party");d="";for(j=0,k=h.length;j<k;j++){e=h[j];i=h[e];d+="<option val="+i+">"+i+"</option>\n"}a.no_party_msg==="Decline to state"&&(d+='<option val="Decline to state">Decline to state</option>\n');b.append(d)}a.requires_party&&$("#party").attr("data-required",!0);a.requires_party&&$("#party").attr("data-required",!0);g=a.id_min_length||0;f=a.id_max_length||100;$("#id_number").attr("data-maxlength",f).attr("data-minlength",g);return c()},error:function(a){}})}})).call(this);