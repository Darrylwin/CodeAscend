import 'package:flutter/material.dart';

/// RouteObserver global partagé entre toutes les pages. pour éviter les dépendances circulaires.
final RouteObserver<ModalRoute<void>> routeObserver =
    RouteObserver<ModalRoute<void>>();