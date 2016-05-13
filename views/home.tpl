<!DOCTYPE html>
<html>
  <head>
    <title>Fibonacci App</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <!-- <meta http-equiv="refresh" content="10"> -->
    <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon"> 
    <link type="text/css" rel="stylesheet" href="/static/style.css">
    <link type="text/css" rel="stylesheet" href="http://cdn.datatables.net/1.10.2/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
  </head>
  <body>
 	
 		
  	<div class="container">
	    
	   
	    <div class="container" >
		    <h1>Fibonacci app</h1>
		    
		    <form class="form-inline" role="form">
			  <div class="form-group">
			    <div class="input-group">
			      <label class="sr-only" for="gen_fib">Sequence Number</label>
			      <input type="text" class="form-control" id="gen_fib" name="number" placeholder="Enter sequence number here">
			    </div>
			  </div>
			  <br/>
			  <button type="button" id="submit_button" class="btn btn-default">Calculer</button>
			</form>
			<br/>
			<div id="result">
			</div>
		    <br/>
		 	<table id="messages" class="display" cellspacing="0">
		        <thead>
		            <tr>
		        	 	<th>sequence id</th>
		                <th>sequence value</th>
		                <th>date created</th>
		            </tr>
		        </thead>
		 
		        <tfoot>
		            <tr>
		                <th>sequence id</th>
		                <th>sequence value</th>
		                <th>date created</th>              
		            </tr>
		        </tfoot>
		 
		        <tbody>
		        </tbody>
			</table>
		</div>
		
    </div>
	
	
	 
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="http://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
    <script type="text/javascript" src="/static/main.js"></script>
    
        	
   <body>
</html>
