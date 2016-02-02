<?php
    /**
     * This file is intended to be used on an external web server somewhere. Its purpose is to keep your consumer secret
     * well, secret. You will need to fill in the values of TB_REQUEST_KEY and TB_CONSUMER_SECRET as follows:
     *
     * - TB_REQUEST_KEY is a key that must be passed as a GET parameter to this script, used as authorization. Never 
     *   make it public. Ever. I strongly recommend you assign a string of at least 32 hex digits to this.
     * - TB_CONSUMER_SECRET is your application's consumer secret that you're protecting. It will be sent back to the
     *   requester if they provide the correct request key.
     */
    
    define("TB_REQUEST_KEY", "");
    
    define("TB_CONSUMER_SECRET", "");
    
    /* STOP EDITING HERE. The rest of this script is what deals with the request. You don't need to change it. */
    
    if(isset($_GET["request_key"]) && $_GET["request_key"] === TB_REQUEST_KEY) {
        $json = array("secret" => TB_CONSUMER_SECRET);
        echo json_encode($json);
    }
    else {
        $json = array("error" => "Access Denied", "error_message" => "The request did not provide the correct access key.");
        echo json_encode($json);
    }
    
?>