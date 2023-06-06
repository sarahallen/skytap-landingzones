
###########################################     FUNCTIONS   ########################################
// Simplifies get requests to system.
// r = endpoints
Function get_skytap ($r) {
    $path = if($r -match $uri){$r} else { $uri + $r}
    $result = Invoke-RestMethod -uri $path
    return, $result
}
// Simplifies setting things like environment runstate, adding vm, etc.
Function set_skytap ($pth, $jsn, $method) {
    $path = if($pth -match $uri){$pth} else {$uri + $pth}
    $json = $jsn | convertto-json
    $action = if($method -ne $null){$method} else {'POST'}
    Invoke-RestMethod -uri $path -WebSession $session -Method $action -body $json -ContentType $content
}
// check for runstate
Function busyness ($b){
    $i = 0
    $check = get_skytap $b
    while($i -ne 3 -and $check.busy -ne $null){
    # No Attribute busy; is this a pre-defined variable?
        write-output 'inside while'
        $i++
        $check = get_skytap $b
        sleep $delay
    }
    return, $check
}

// If template in a busy state, it won't copy
if((get_skytap $create_template.url).busy -ne $null ){ 
    busyness $create_template.url
}