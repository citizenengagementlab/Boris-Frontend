var hash=document.location.hash;$(document).ready(function(){if(hash==="#tab"){$(".tabs").tab("show");$(".tabs").show();$("form").addClass("tab-content");$("#tab-new, #tab-personal , #tab-additional, #tab-action").addClass("tab-pane");$("h1").removeAttr("data-toggle");$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");$("button.continue").removeAttr("data-toggle")}else if(hash==="#accordion"){$(".tabs").hide();$("#tab-link").removeAttr("data-toggle")}else{$(".tabs").hide();$("h1").removeAttr("data-toggle");$("#accordion-new, #accordion-personal, #accordion-additional, #accordion-action").removeClass("collapse");$("button.continue").hide()}$(".mailing").css("display","none");$(".name-change").css("display","none");$(".address-change").css("display","none");$("#has_mailing_address").click(function(){$("#has_mailing_address").is(":checked")?$(".mailing").fadeIn():$(".mailing").fadeOut()});$("#change_of_name").click(function(){$("#change_of_name").is(":checked")?$(".name-change").fadeIn():$(".name-change").fadeOut()});$("#change_of_address").click(function(){$("#change_of_address").is(":checked")?$(".address-change").fadeIn():$(".address-change").fadeOut()});$("#email_address").live("keyup",function(){$.ajax({type:"get",url:"https://rtvstaging2.osuosl.org/api/v1/state_requirements.json?lang=en&home_zip_code=94608",data:this.data,dataType:"jsonp",success:function(a){alert(a)},error:function(a){alert(a)},cache:!1})});$(".tab-link").click(function(){var a=$(this).attr("href");$("a[href="+a+"]").tab("show");delete a})});