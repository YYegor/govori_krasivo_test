	
  
window.onload = config_load();

function g_progress_plus(e)
	{
		//add more stars to the progress ⭐
		console.log("Progress +1");
		$("#gamef").text($("#gamef").text() + "⭐").fadeIn(500);
	}
function config_load(e)
		{
			// init all: hide all text bubbles
			$("#video1_text_div").hide();
			$("#video1_uaction_div").hide();
			$("#video1_div").hide();
			
			$("#video2_text").hide();
			$("#video2_uaction_div").hide();
			$("#video2_div").hide();

			$("#video3_uaction_div").hide();
			$("#video3_div").hide();
			$("#video3_text").hide();
			

			//read config and load content from json
			
			var module_duration = 3;

			var mydata = JSON.parse(data);
			console.log("config loaded");

			$("#video1_text").html(mydata[0].module1_text);
			$("#video1_uaction").html(mydata[0].module1_uaction);
			$("#video1").attr("src","static/video\\"+mydata[0].module1_video);

			$("#video2_text").html(mydata[0].module2_text);
			$("#video2_uaction").html(mydata[0].module2_uaction);
			$("#video2").attr("src","static/video\\"+mydata[0].module2_video);
			
			$("#video3_text").html(mydata[0].module3_text);
			$("#video3_uaction").html(mydata[0].module3_uaction);
			$("#video3").attr("src", "static/video\\"+mydata[0].module3_video);
			
			// all elements are hidden
			
			$("#video1_text_div").delay(5000).show();
			$("#video1_uaction_div").show();
			$("#video1_uaction").click(function (e){ $("#video1_div").show(); $("html, body").animate({scrollTop: $("#video1_div").offset().top}, 2000);} );
			$("#video1").on("ended",function(){$("#video2_text").show(); $("#video2_uaction_div").fadeIn(500); g_progress_plus(); });

			$("#video2_uaction").click(function (e){ $("#video2_div").show(); $("html, body").animate({scrollTop: $("#video2_div").offset().top}, 2000);} );
			$("#video2").on("ended",function(){$("#video3_text").show(); $("#video3_uaction_div").fadeIn(500); $("html, body").animate({scrollTop: $("#video3_text").offset().top}, 2000); g_progress_plus();});			

			$("#video3_uaction").click(function (e){ $("#video3_div").show(); $("html, body").animate({scrollTop: $("#video3_div").offset().top}, 2000);} );
			$("#video3").on("ended", g_progress_plus());						

			console.log("config ended");

		}
