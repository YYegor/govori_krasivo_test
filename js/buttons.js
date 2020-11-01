	
    var v2 = document.getElementById('video_1');
	
	if (v2)
		{
			v2.addEventListener('ended',myHandler_1,true);
			//alert("listner ok");
		}
	
    function myHandler_1(e) {
        document.getElementById('mod2').style.display = "block";
		document.getElementById('video_2').play();
		//alert("handl");
	
    }
    
	var v2 = document.getElementById('video_2');
	
	if (v2)
		{
			v2.addEventListener('ended',myHandler_2,true);
			//alert("listner ok");
		}
	
    function myHandler_2(e) {
        document.getElementById('mod3').style.display = "block";
		document.getElementById('video_3').play();
		//alert("handl");
		}

window.onload = config_load();

function config_load(e)
		{
			// init all: hide all text bubbles
			
			//read config and load content from json
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
			$("#video1_text_div").show();
			$("#video1_uaction_div").show();
			$("#video1_uaction").click(function (e){ $("#video1_div").show();} );

			//$("#video1_div").show();
			
			//$("#video2_text").show();
			//$("#video2_uaction_div").show();
			//$("#video2_div").show();

			//$("#video3_uaction_div").show();
			//$("#video3_div").show();
			//$("#video3_text").show();
			
		}
