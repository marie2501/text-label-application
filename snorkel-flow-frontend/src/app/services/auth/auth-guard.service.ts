import {ActivatedRouteSnapshot, CanActivateFn, RouterStateSnapshot} from "@angular/router";

export const loginGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot) => {
    //todo Logik einbauen sobald Login funktioniert
    return true;
}
