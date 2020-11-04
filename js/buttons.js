	
  
window.onload = config_load();

function config_load(e)
		{
			// init all: hide all text bubbles
			
			//read config and load content from json
			console.log("loaded");
			$("#video1_text_div").hide();
			$("#video1_uaction_div").hide();
			$("#video1_div").hide();
			
			$("#video2_text").hide();
			$("#video2_uaction_div").hide();
			$("#video2_div").hide();

			$("#video3_uaction_div").hide();
			$("#video3_div").hide();
			$("#video3_text").hide();

			var mydata = JSON.parse(data);
			document.getElementById('video1_text').innerHTML  = mydata[0].module1_text;
			document.getElementById('video1_uaction').innerHTML  = mydata[0].module1_uaction;
			document.getElementById('video1').src  = "video\\"+mydata[0].module1_video;

			document.getElementById('video2_text').innerHTML  = mydata[1].module2_text;
			document.getElementById('video2_uaction').innerHTML  = mydata[1].module2_uaction;
			document.getElementById('video2').src  = "video\\"+mydata[1].module2_video;
			
			document.getElementById('video3_text').innerHTML  = mydata[2].module3_text;
			document.getElementById('video3_uaction').innerHTML  = mydata[2].module3_uaction;
			document.getElementById('video3').src  = "video\\"+mydata[2].module3_video;
			
			$("#video1_text_div").delay(5000).show();
			$("#video1_uaction_div").show();
			$("#video1_uaction").click(function (e){ $("#video1_div").show(); $('html, body').animate({scrollTop: $("#video1_div").offset().top}, 2000);} );
			$("#video1").on('ended',function(){$("#video2_text").show(); $("#video2_uaction_div").fadeIn(500);});

			$("#video2_uaction").click(function (e){ $("#video2_div").show(); $('html, body').animate({scrollTop: $("#video2_div").offset().top}, 2000);} );
			$("#video2").on('ended',function(){$("#video3_text").show(); $("#video3_uaction_div").fadeIn(500); $('html, body').animate({scrollTop: $("#video3_text").offset().top}, 2000);});			

			$("#video3_uaction").click(function (e){ $("#video3_div").show(); $('html, body').animate({scrollTop: $("#video3_div").offset().top}, 2000);} );
			

			console.log("config ended");

		}
