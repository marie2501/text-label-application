import {ActivatedRouteSnapshot, CanActivateChildFn, CanActivateFn, Router, RouterStateSnapshot} from "@angular/router";
import {inject} from "@angular/core";
import {WorkflowService} from "../workflow/workflow.service";
import {tap} from "rxjs";
import {RunService} from "../workflow/run.service";

export const loginGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  const router = inject(Router);
  if (localStorage.getItem('userData')) {
    return true;
  }
  return router.createUrlTree(['/login']);
}

export const loginGuardHomepage: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  const router = inject(Router);
  if (localStorage.getItem('userData')) {
    return router.createUrlTree(['/dashboard']);
  }
  return true;
}

export const workflowAccessGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  const router = inject(Router);
  const workflowService = inject(WorkflowService);
  const workflow_id = next.params['wid'];
  return workflowService.accessWorkflow(workflow_id).pipe(tap(access => {
    if(access){
      return true
    } else {
      const urlTree = router.createUrlTree(['/forbidden']);
      router.navigateByUrl(urlTree);
      return false
    }
  }));
}

export const runAccessGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  const router = inject(Router);
  const runService = inject(RunService);
  let run_id = next.params['runID'];
  if (run_id == undefined){
    run_id = next.parent?.params['runID'];
  }
  return runService.accessRun(run_id).pipe(tap(access => {
    if(access){
      return true
    } else {
      const urlTree = router.createUrlTree(['/forbidden']);
      router.navigateByUrl(urlTree);
      return false
    }
  }));
}
