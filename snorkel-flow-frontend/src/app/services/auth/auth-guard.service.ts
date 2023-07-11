import {ActivatedRouteSnapshot, CanActivateChildFn, CanActivateFn, RouterStateSnapshot} from "@angular/router";

export const loginGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
    if (localStorage.getItem('userData')) {
      return true;
    }
    return false;
}


export const loginChildGuard: CanActivateChildFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  return loginGuard(next, state);
}

//todo return URLTree um auf /dashboard zu bleiben
export const loginGuardHomepage: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
  if (localStorage.getItem('userData')) {
    return false;
  }
  return true;
}
